from __future__ import annotations

import contextlib
import functools
import hashlib
import inspect
import itertools
import shutil
import tempfile
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

import pyarrow as pa
import pyarrow.dataset as ds
from pyarrow.dataset import field as pyarrow_field
from pyarrow.dataset import scalar as pyarrow_scalar

from zense import config

try:
    import pandas as pd
    from pandas import DataFrame as DataFrameType
except ImportError:
    pd = None
    DataFrameType = None


SourceType = Union[str, List[str], Union[Path, List[Path]], "Dataset", List["Dataset"]]

DEFAULT_BATCH_SIZE = 131_072
DEFAULT_FORMAT = "arrow"


def mapfunc(func):
    @functools.wraps(func)
    def wrapped(*args, **kwargs):
        output = func(*args, **kwargs)
        if isinstance(output, pd.Series):
            return output
        return pd.Series(output)

    return wrapped


class Expression:
    def __init__(self, expression: Union[Expression, ds.Expression]):
        if isinstance(expression, Expression):
            expression = expression._wrapped
        self._wrapped: ds.Expression = expression

    def __eq__(self, other: Any) -> Expression:
        return Expression(self._wrapped == Expression(other)._wrapped)

    def __ne__(self, other: Any) -> Expression:
        return Expression(self._wrapped != Expression(other)._wrapped)

    def __lt__(self, other: Any) -> Expression:
        return Expression(self._wrapped < Expression(other)._wrapped)

    def __le__(self, other: Any) -> Expression:
        return Expression(self._wrapped <= Expression(other)._wrapped)

    def __gt__(self, other: Any) -> Expression:
        return Expression(self._wrapped > Expression(other)._wrapped)

    def __ge__(self, other: Any) -> Expression:
        return Expression(self._wrapped >= Expression(other)._wrapped)

    def __and__(self, other: Any) -> Expression:
        return Expression(self._wrapped & Expression(other)._wrapped)

    def __or__(self, other: Any) -> Expression:
        return Expression(self._wrapped | Expression(other)._wrapped)

    def __invert__(self) -> Expression:
        return Expression(~self._wrapped)

    def is_nan(self) -> Expression:
        return Expression(self._wrapped.is_nan())

    def is_null(self, nan_is_null: bool = False):
        return Expression(self._wrapped.is_null(nan_is_null=nan_is_null))

    def is_valid(self) -> Expression:
        return Expression(self._wrapped.is_valid())

    def isin(self, other: Expression) -> Expression:
        return Expression(self._wrapped.isin(Expression(other)._wrapped))

    def equals(self, other: Expression) -> Expression:
        return Expression(self._wrapped.equals(Expression(other)._wrapped))

    def __hash__(self) -> int:
        return hash(self._wrapped)

    def __repr__(self) -> str:
        return f"Expression({self._wrapped})"

    def to_pyarrow(self) -> ds.Expression:
        return self._wrapped

    @classmethod
    def field(cls, *name_or_index: Tuple[str]) -> Expression:
        field = pyarrow_field(*name_or_index)
        return cls(field)

    @classmethod
    def scalar(cls, value: Any) -> Expression:
        scaler = pyarrow_scalar(value)
        return cls(scaler)


class Dataset:
    def __init__(
        self,
        data: Union[DataFrameType, List[dict], Dict[str, list]] = None,
        path: Optional[Union[str, Path]] = None,
        format: str = DEFAULT_FORMAT,
        cache_dir: Optional[Union[str, Path]] = None,
    ):
        # private attributes
        if path is None:
            # create a temporary directory in system temp directory
            cache_dir = Path(config.resources.path).expanduser() / "cache" / "datasets"
            if not cache_dir.exists():
                cache_dir.mkdir(parents=True, exist_ok=True)
            path = Path(tempfile.mkdtemp(dir=cache_dir))
        data_path = get_data_path(path)
        self._path = path
        self._format = format
        ds.write_dataset(pa.table(data), data_path, format=format)
        self._wrapped: ds.Dataset = ds.dataset(data_path, format=self._format)

    @classmethod
    def load_dataset(
        cls,
        path: Union[Path, str],
        format: str = DEFAULT_FORMAT,
    ) -> Dataset:
        # create instance using __new__
        inst = cls.__new__(cls)
        inst._path = path
        inst._format = format
        inst._wrapped = ds.dataset(
            get_data_path(path),
            format=inst._format,
        )
        return inst

    @property
    def path(self) -> Path:
        return self._path

    @property
    def format(self) -> str:
        return self._format

    @property
    def _wrapped_format_default_extname(self) -> str:
        return self._wrapped.format.default_extname

    def count_rows(self) -> int:
        return self._wrapped.count_rows()

    def head(
        self,
        num_rows: int = 5,
        columns: Union[str, List[str], None] = None,
        filter: Expression = None,
        batch_size: int = DEFAULT_BATCH_SIZE,
    ) -> DataFrameType:
        filter = filter.to_pyarrow() if filter else None
        if isinstance(columns, str):
            columns = [columns]
        table: pa.Table = self._wrapped.head(
            num_rows=num_rows,
            columns=columns,
            filter=filter,
            batch_size=batch_size,
        )
        return table.to_pandas()

    def map(
        self,
        func: Any,
        batch_size: int = DEFAULT_BATCH_SIZE,
    ) -> Dataset:
        data_iter = (
            pa.RecordBatch.from_pandas(
                batch.to_pandas().apply(
                    mapfunc(func),
                    axis=1,
                ),
            )
            for batch in self._wrapped.to_batches(batch_size=batch_size)
        )
        try:
            first: pa.RecordBatch = next(data_iter)
        except StopIteration:
            first = None
        data_iter = itertools.chain([first], data_iter)
        name = hashlib.sha256(inspect.getsource(func).encode()).hexdigest()
        schema = None if first is None else first.schema
        return self._sync_pyarrow_dataset(f"mapped-{name}", data_iter, schema)

    def filter(self, expression: Expression = None) -> Dataset:
        if expression is None:
            return self
        pyarrow_expression = expression.to_pyarrow()
        data = self._wrapped.filter(pyarrow_expression)
        name = hashlib.sha256(str(pyarrow_expression).encode()).hexdigest()
        schema = data.schema
        return self._sync_pyarrow_dataset(f"filter-{name}", data, schema)

    def _sync_pyarrow_dataset(
        self,
        suffix: Union[str, Path],
        data: Union[
            ds.Dataset,
            pa.RecordBatch,
            pa.Table,
            List[pa.RecordBatch],
            List[pa.Table],
        ],
        schema: pa.Schema,
    ) -> Dataset:
        path = self.path / suffix
        if not path.exists():
            data_path = get_data_path(path)
            ds.write_dataset(
                data,
                data_path,
                schema=schema,
                format=self.format,
            )
        return type(self).load_dataset(path)

    def cleanup(self):
        if not self.path.exists():
            return
        shutil.rmtree(self.path)

    def __enter__(self) -> Dataset:
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        with contextlib.suppress(Exception):
            self.cleanup()


def get_data_path(path: Union[Path, str]) -> Path:
    if isinstance(path, str):
        path = Path(path)
    if path.is_dir() or not path.exists():
        path.mkdir(
            parents=True,
            exist_ok=True,
        )
        data_path = path / "data"
    else:
        msg = f"expected path to be directory, got '{path}'"
        raise ValueError(msg)
    return data_path

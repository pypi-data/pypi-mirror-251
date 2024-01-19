from octoflow import Config
from zense.dataset import Dataset

__all__ = [
    "Dataset",
]

config = Config()

config.update(
    {
        "resources": {
            "path": "~/.zense",
        }
    }
)

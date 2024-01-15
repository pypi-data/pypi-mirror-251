import collections
import contextlib
import io
import json
import sys
from abc import ABC
from abc import abstractmethod
from pathlib import Path
from typing import *

import attrs
import validators

# Todo: Make this optional and configurable
try:
    import requests_cache
    requests = requests_cache.CachedSession("BrokenDotmap")
except ImportError:
    import requests

class Utils:

    @staticmethod
    def is_dunder(name: str) -> bool:
        return name.startswith("__") and name.endswith("__")

    @staticmethod
    def true_path(path: Optional[Path]) -> Optional[Path]:
        return Path(path).resolve().expanduser() if path else None

    @staticmethod
    def mkdir(path: Path, parent: bool=True) -> Path:
        path = Utils.true_path(path)
        (path.parent if parent else path).mkdir(parents=True, exist_ok=True)
        return path

    @staticmethod
    def non_empty_file(path: Path) -> bool:
        return path.exists() and path.is_file() and path.stat().st_size > 0

    @staticmethod
    def empty_file(path: Path, create: bool=True) -> bool:
        if create and not path.exists():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.touch()
        return path.exists() and path.is_file() and len(path.read_text()) == 0

    @staticmethod
    def empty_path(path: Path) -> bool:
        return not path.exists()

# Do we have a module?
have_import = lambda module: module in sys.modules

# isort: off
from .BaseLoader import *
from .BrokenDotmap import *
from .Loaders import *

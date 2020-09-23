import attr
import importlib
from typing import Callable
import pandas as pd


def has_import(module: str) -> bool:
    has_module = importlib.util.find_spec(module) is not None  # type: ignore
    if has_module:
        importlib.import_module(module)
    return has_module


@attr.s
class PandasFlags:
    has_swifter = has_import("swifter")
    _use_swifter = attr.ib(default=has_swifter)

    @property
    def use_swifter(self) -> bool:
        return self._use_swifter

    @use_swifter.setter
    def use_swifter(self, value: bool) -> None:
        if value is True and not self.has_swifter:
            raise ImportError("Swifter not currently installed")

        self._use_swifter = value


_pandas_flags = PandasFlags()


def pandas_apply(series: pd.Series) -> Callable:
    return series.swifter.apply if _pandas_flags.use_swifter else series.apply

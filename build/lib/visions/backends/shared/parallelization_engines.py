from typing import Callable, List, Type

import attr
import pandas as pd

from visions.backends.shared.utilities import has_import


@attr.s
class Engine:
    name = attr.ib()

    @classmethod
    def setup(cls, *args, **kwargs) -> None:
        raise NotImplementedError("No setup defined for generic engine")

    @staticmethod
    def apply(series: pd.Series) -> Callable[[Callable], pd.Series]:
        raise NotImplementedError("No apply defined for generic engine")


class PandasEngine(Engine):
    name = "pandas"
    _is_setup = True

    @classmethod
    def setup(cls, *args, **kwargs) -> None:
        pass

    @staticmethod
    def apply(series: pd.Series) -> Callable[[Callable], pd.Series]:
        return series.apply


class SwifterEngine(Engine):
    name = "swifter"
    _is_setup = False

    @classmethod
    def setup(cls, *args, **kwargs) -> None:
        if cls._is_setup:
            return

        import swifter

        cls._is_setup = True

    @staticmethod
    def apply(series: pd.Series) -> Callable[[Callable], pd.Series]:
        return series.swifter.apply


_PANDAS_ENGINES = [PandasEngine, SwifterEngine]


class EngineCollection:
    def __init__(self, engines: List[Type[Engine]]):
        self.engines = {engine.name: engine for engine in engines}

    def is_engine(self, name: str) -> bool:
        return name in self.engines

    def get(self, name: str) -> Type[Engine]:
        return self.engines[name]


class PandasApply:
    supported_engines = EngineCollection(
        [engine for engine in _PANDAS_ENGINES if hasattr(engine, "apply")]
    )
    _engine: Type[Engine] = PandasEngine

    @property
    def engine(self) -> Type[Engine]:
        return self._engine

    @engine.setter
    def engine(self, value: str, *args, **kwargs) -> None:
        if not self.supported_engines.is_engine(value):
            raise ValueError(f"{value} is not a supported pandas apply engine")
        self._engine = self.supported_engines.get(value)
        self._engine.setup(*args, **kwargs)

    @property
    def apply(self) -> Callable[[pd.Series], Callable[[Callable], pd.Series]]:
        return self.engine.apply


class PandasHandler:
    def __init__(self):
        self.has_swifter = has_import("swifter")

        self.applier = PandasApply()
        self._set_default_apply_engine()

    def _set_default_apply_engine(self) -> None:
        if self.has_swifter:
            self.applier.engine = "swifter"


_pandas_handler = PandasHandler()


def pandas_apply(series: pd.Series, func: Callable) -> pd.Series:
    return _pandas_handler.applier.apply(series)(func)

import attr
import importlib
from typing import Callable, Type, List
import pandas as pd


def has_import(module: str) -> bool:
    has_module = importlib.util.find_spec(module) is not None  # type: ignore
    return has_module


@attr.s
class Engine:
    name = attr.ib()

    @classmethod
    def setup(cls, *args, **kwargs) -> None:
        raise NotImplemented("No setup defined for generic engine")

    @staticmethod
    def apply(series: pd.Series) -> Callable:
        raise NotImplemented("No apply defined for generic engine")


class PandasEngine(Engine):
    name = "pandas"
    _is_setup = False

    @classmethod
    def setup(cls, *args, **kwargs) -> None:
        pass

    @staticmethod
    def apply(series: pd.Series) -> Callable:
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
    def apply(series: pd.Series) -> Callable:
        return series.swifter.apply


class PandarallelEngine(Engine):
    name = "pandarallel"
    _is_setup = False

    @classmethod
    def setup(cls, *args, **kwargs) -> None:
        if cls._is_setup:
            return

        from pandarallel import pandarallel

        pandarallel.initialize(*args)
        cls._is_setup = True

    @staticmethod
    def apply(series: pd.Series) -> Callable:
        return series.parallel_apply


_PANDAS_ENGINES = [PandasEngine, SwifterEngine, PandarallelEngine]


class PandasEnginesCollection:
    def __init__(self, engines: List[Type[Engine]]):
        self.engines = {engine.name: engine for engine in engines}

    def is_engine(self, name) -> bool:
        return name in self.engines

    def get(self, name) -> Type[Engine]:
        return self.engines[name]


class PandasApply:
    supported_engines = PandasEnginesCollection(
        [engine for engine in _PANDAS_ENGINES if hasattr(engine, "apply")]
    )
    _engine: Type[Engine] = PandasEngine

    @property
    def engine(self) -> Type[Engine]:
        return self._engine

    @engine.setter
    def engine(self, value: str, *args, **kwargs) -> None:
        if not self.supported_engines.is_engine(value):
            raise Exception(f"{value} is not a supported pandas apply engine")
        self._engine = self.supported_engines.get(value)
        self._engine.setup(*args, **kwargs)

    @property
    def apply(self) -> Callable:
        return self.engine.apply


class PandasHandler:
    def __init__(self):
        self.has_swifter = has_import("swifter")
        self.has_pandarallel = has_import("pandarallel")

        self.applier = PandasApply()
        self._set_default_apply_engine()

    def _set_default_apply_engine(self) -> None:
        if self.has_swifter:
            self.applier.engine = "swifter"
        # if self.has_pandarallel:
        #    self.applier.engine = 'pandarallel'


_pandas_handler = PandasHandler()


def pandas_apply(series: pd.Series) -> Callable:
    return _pandas_handler.applier.apply(series)

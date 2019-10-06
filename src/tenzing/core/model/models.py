from abc import abstractmethod, ABCMeta
import pandas as pd


class meta_model(ABCMeta):
    def __contains__(cls, series: pd.Series) -> bool:
        if series.empty:
            from tenzing.core.model.types.tenzing_generic import tenzing_generic

            return cls == tenzing_generic
        return cls.contains_op(series)

    def __str__(cls) -> str:
        return f"{cls.__name__}"

    def __repr__(cls) -> str:
        return str(cls)


class tenzing_model(metaclass=meta_model):
    """Abstract implementation of a tenzing type.

    Provides a common API for building custom tenzing datatypes.
    """

    @classmethod
    @abstractmethod
    def get_relations(cls) -> dict:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def contains_op(cls, series: pd.Series) -> bool:
        raise NotImplementedError

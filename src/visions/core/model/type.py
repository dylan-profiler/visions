from abc import abstractmethod, ABCMeta
from typing import Sequence
import pandas as pd

from visions.core.model.relations import TypeRelation


class VisionsBaseTypeMeta(ABCMeta):
    def __contains__(cls, series: pd.Series) -> bool:
        if series.empty:
            from visions.core.implementations.types import visions_generic

            return cls == visions_generic
        return cls.contains_op(series)  # type: ignore

    def __str__(cls) -> str:
        return f"{cls.__name__}"

    def __repr__(cls) -> str:
        return str(cls)


class VisionsBaseType(metaclass=VisionsBaseTypeMeta):
    """Abstract implementation of a vision type.

    Provides a common API for building custom visions data types.
    """

    @classmethod
    @abstractmethod
    def get_relations(cls) -> Sequence[TypeRelation]:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def contains_op(cls, series: pd.Series) -> bool:
        raise NotImplementedError

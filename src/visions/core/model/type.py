from abc import abstractmethod, ABCMeta
from typing import Sequence, Type, Callable

import attr
import pandas as pd


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
    def get_relations(cls) -> Sequence["TypeRelation"]:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def contains_op(cls, series: pd.Series) -> bool:
        raise NotImplementedError


@attr.s(frozen=True)
class TypeRelation:
    """Relationship encoder between implementations of :class:`visions.core.models.VisionsBaseType`

    Defines a one to one relationship between two VisionsBaseType implementations,
    A and B, with respect to an underlying data series. In order to define a relationship we need
    two methods:

        - **is_relationship**, determines whether a series of type B can be alternatively represented as type A.
        - **transform**, provides a mechanism to convert the series from B -> A.

    For example, the series `pd.Series([1.0, 2.0, 3.0])` is encoded as a sequence of
    floats but in reality they are all integers.

    Examples:
        >>> from visions.core.implementations.types import visions_integer, visions_float
        >>> x = pd.Series([1.0, 2.0, 3.0])
        >>> relation = TypeRelation(visions_integer, visions_float)
        >>> relation.is_relation(x)
        True

        >>> relation.transform(x)
        pd.Series([1, 2, 3])
    """

    type: Type[VisionsBaseType] = attr.ib()
    related_type: Type[VisionsBaseType] = attr.ib()
    inferential: bool = attr.ib()
    transformer: Callable = attr.ib()
    relationship: Callable = attr.ib(default=lambda x: False)

    def is_relation(self, series: pd.Series) -> bool:
        return self.relationship(series)

    def transform(self, series: pd.Series) -> pd.Series:
        return self.transformer(series)

    def __repr__(self) -> str:
        return f"TypeRelation({self.related_type} -> {self.type})"

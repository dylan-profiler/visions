from collections import namedtuple
import typing
from typing import Callable, Optional, Type
import attr

import pandas as pd


def identity_relation(series: pd.Series) -> pd.Series:
    return series


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

    type: Type["visions.core.model.type.VisionsBaseType"] = attr.ib()
    related_type: Type["visions.core.model.type.VisionsBaseType"] = attr.ib()
    inferential: bool = attr.ib()
    transformer: Callable = attr.ib()
    relationship: Callable = attr.ib(default=lambda x: False)

    def is_relation(self, series: pd.Series) -> bool:
        return self.relationship(series)

    def transform(self, series: pd.Series) -> pd.Series:
        return self.transformer(series)

    def __repr__(self) -> str:
        return f"TypeRelation({self.related_type} -> {self.type})"


class IdentityRelation(TypeRelation):
    def __init__(self, type, related_type, relationship=None):
        relationship = type.__contains__ if relationship is None else relationship
        super().__init__(
            type,
            related_type,
            relationship=relationship,
            transformer=identity_relation,
            inferential=False,
        )

    def __repr__(self) -> str:
        return f"IdentityRelation({self.related_type} -> {self.type})"


class InferenceRelation(TypeRelation):
    def __init__(self, type, related_type, transformer, relationship=None):
        relationship = type.__contains__ if relationship is None else relationship
        super().__init__(
            type,
            related_type,
            relationship=relationship,
            transformer=transformer,
            inferential=True,
        )

    def __repr__(self) -> str:
        return f"InferenceRelation({self.related_type} -> {self.type})"

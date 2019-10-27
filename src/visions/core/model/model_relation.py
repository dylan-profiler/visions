from collections import namedtuple
from typing import Callable, Optional, Type

import pandas as pd

relation_conf = namedtuple(
    "relation_conf",
    ("inferential", "relationship", "transformer"),
    defaults=(None, None),
)


class model_relation:
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
        >>> relation = model_relation(visions_integer, visions_float)
        >>> relation.is_relation(x)
        True

        >>> relation.transform(x)
        pd.Series([1, 2, 3])
    """

    def __init__(
        self,
        model,
        friend_model,
        inferential: bool,
        relationship: Optional[Callable] = None,
        transformer: Optional[Callable] = None,
    ):
        self.model = model
        self.friend_model = friend_model
        self.inferential = inferential
        if inferential:
            if transformer is None or relationship is None:
                raise ValueError(
                    "Inferential relations should have transformer and relations"
                )
            self.relationship = relationship
            self.transformer = transformer
        else:
            if transformer is not None or relationship is not None:
                raise ValueError(
                    "noninferential relations may not have transformer or relations"
                )

            self.relationship = self.model.__contains__
            self.transformer = lambda s: s

    def is_relation(self, series: pd.Series) -> bool:
        return self.relationship(series)

    def transform(self, series: pd.Series) -> pd.Series:
        return self.transformer(series)

    def __repr__(self) -> str:
        return f"({self.friend_model} -> {self.model})"

    def __eq__(self, other) -> bool:
        return isinstance(other, model_relation) and str(self) == str(other)

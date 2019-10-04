from collections import namedtuple

import pandas as pd


relation_conf = namedtuple('relation_conf', ('inferential', 'map'), defaults=(None, None,))


class model_relation:
    """Relationship encoder between implementations of :class:`tenzing.core.models.tenzing_model`

    Defines a one to one relationship between two tenzing_model implementations,
    A and B, with respect to an underlying data series. In order to define a relationship we need
    two methods:

        - **is_relationship**, determines whether a series of type B can be alternatively represented as type A.
        - **transform**, provides a mechanism to convert the series from B -> A.

    For example, the series `pd.Series([1.0, 2.0, 3.0])` is encoded as a sequence of
    floats but in reality they are all integers.

    Examples:
        >>> from tenzing.core.model.types import tenzing_integer, tenzing_float
        >>> x = pd.Series([1.0, 2.0, 3.0])
        >>> relation = model_relation(tenzing_integer, tenzing_float)
        >>> relation.is_relation(x)
        True

        >>> relation.transform(x)
        pd.Series([1, 2, 3])
    """

    def __init__(
        self, model, friend_model, relationship=None, transformer=None, inferential=None
    ):
        """
        Args:
            model: The type this relation will transform a series into.
            friend_model: The type this relation will transform a series from.
            relationship: A method to determine if a series of friend_model type can be converted to type model.
            transformer: A method to convert a series from type friend_model to type model.
        """
        self.model = model
        self.friend_model = friend_model
        self.edge = (self.friend_model, self.model)
        self.relationship = relationship if relationship else self.model.__contains__
        self.transformer = transformer
        self.inferential = inferential

    def is_relation(self, obj: pd.Series) -> bool:
        return self.relationship(obj)

    def transform(self, obj: pd.Series) -> pd.Series:
        return self.model.cast(obj, self.transformer)

    def __repr__(self) -> str:
        return f"({self.friend_model} -> {self.model})"

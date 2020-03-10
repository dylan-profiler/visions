import pandas as pd
import attr


def identity_relation(series: pd.Series) -> pd.Series:
    return series


@attr.s(frozen=True)
class TypeRelation:
    """Relationship encoder between implementations of :class:`visions.types.type.VisionsBaseType`

    Defines a one to one relationship between two VisionsBaseType implementations,
    A and B, with respect to an underlying data series. In order to define a relationship we need
    two methods:

        - **is_relationship**, determines whether a series of type B can be alternatively represented as type A.
        - **transform**, provides a mechanism to convert the series from B -> A.

    For example, the series `pd.Series([1.0, 2.0, 3.0])` is encoded as a sequence of
    floats but in reality they are all integers.

    Examples:
        >>> from visions.types import Integer, Float
        >>> x = pd.Series([1.0, 2.0, 3.0])
        >>> relation = TypeRelation(Integer, Float)
        >>> relation.is_relation(x)
        True

        >>> relation.transform(x)
        pd.Series([1, 2, 3])
    """

    type = attr.ib()
    related_type = attr.ib()
    inferential = attr.ib()
    transformer = attr.ib()
    relationship = attr.ib(default=lambda x: False)

    def is_relation(self, series: pd.Series) -> bool:
        return self.relationship(series)

    def transform(self, series: pd.Series) -> pd.Series:
        return self.transformer(series)


@attr.s(frozen=True)
class IdentityRelation(TypeRelation):
    inferential = attr.ib(default=False)
    transformer = attr.ib(default=identity_relation)
    relationship = attr.ib()

    @relationship.default
    def make_relationship(self):
        return self.type.__contains__


@attr.s(frozen=True)
class InferenceRelation(TypeRelation):
    inferential = attr.ib(default=True)
    relationship = attr.ib()

    @relationship.default
    def make_relationship(self):
        return self.type.__contains__

import pandas as pd
import attr

from visions.core.model import TypeRelation


def identity_relation(series: pd.Series) -> pd.Series:
    return series


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

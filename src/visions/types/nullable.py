import pandas as pd

from visions.relations import IdentityRelation
from visions.types.generic import Generic
from visions.types.type import VisionsBaseType


def na_transform(series, state: dict):
    state["hasnans"] = series.hasnans
    if state["hasnans"]:
        series = series.dropna()
    return series


class Optional(VisionsBaseType):
    @classmethod
    def get_relations(cls):
        return [
            IdentityRelation(
                cls,
                NonEmpty,
                transformer=na_transform,
            )
        ]

    @classmethod
    def contains_op(cls, series: pd.Series, state: dict) -> bool:
        return True


class NonEmpty(VisionsBaseType):
    @classmethod
    def get_relations(cls):
        return [IdentityRelation(cls, Generic)]

    @classmethod
    def contains_op(cls, series: pd.Series, state: dict):
        # Alternatively you could use len(series) > 0, in which case
        #  series such as [np.nan] are not recognized as empty
        state["count"] = series.count()
        return state["count"] > 0


class NonMissing(VisionsBaseType):
    @classmethod
    def get_relations(cls):
        return [IdentityRelation(cls, Generic)]

    @classmethod
    def contains_op(cls, series: pd.Series, state: dict):
        return not series.hasnans

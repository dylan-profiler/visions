import pandas as pd

from visions import Generic, VisionsBaseType
from visions.relations import IdentityRelation


class Nominal(VisionsBaseType):
    @classmethod
    def get_relations(cls):
        return [IdentityRelation(Nominal, Generic)]

    @classmethod
    def contains_op(cls, series: pd.Series) -> bool:
        return True

import pandas as pd
import pandas.core.dtypes.common as pdt

from visions import VisionsBaseType
from visions.relations import IdentityRelation
from visions.types.qualitative_quantitative import Quantitative


class Discrete(VisionsBaseType):
    @classmethod
    def get_relations(cls):
        return [IdentityRelation(Discrete, Quantitative)]

    @classmethod
    def contains_op(cls, series: pd.Series) -> bool:
        return pdt.is_integer_dtype(series)

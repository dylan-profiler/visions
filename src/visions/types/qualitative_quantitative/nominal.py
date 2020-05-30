import pandas as pd
import pandas.core.dtypes.common as pdt

from visions import VisionsBaseType
from visions.relations import IdentityRelation
from visions.types.qualitative_quantitative import Qualitative


class Nominal(VisionsBaseType):
    @classmethod
    def get_relations(cls):
        return [IdentityRelation(Nominal, Qualitative)]

    @classmethod
    def contains_op(cls, series: pd.Series) -> bool:
        return not pdt.is_categorical_dtype(series) or not series.cat.ordered

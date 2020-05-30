import pandas as pd
import pandas.core.dtypes.common as pdt

from visions import VisionsBaseType
from visions.relations import IdentityRelation
from visions.types.measurement_level import Interval


class Ratio(VisionsBaseType):
    @classmethod
    def get_relations(cls):
        return [IdentityRelation(Ratio, Interval)]

    @classmethod
    def contains_op(cls, series: pd.Series) -> bool:
        return pdt.is_timedelta64_dtype(series)

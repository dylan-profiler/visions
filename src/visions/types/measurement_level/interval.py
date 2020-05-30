import pandas as pd
import pandas.core.dtypes.common as pdt

from visions import VisionsBaseType
from visions.relations import IdentityRelation
from visions.types.measurement_level import Ordinal


class Interval(VisionsBaseType):
    @classmethod
    def get_relations(cls):
        return [IdentityRelation(Interval, Ordinal)]

    @classmethod
    def contains_op(cls, series: pd.Series) -> bool:
        return pdt.is_numeric_dtype(series) or pdt.is_datetime_or_timedelta_dtype(
            series
        )

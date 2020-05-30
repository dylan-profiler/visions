import pandas as pd
import pandas.core.dtypes.common as pdt

from visions import VisionsBaseType
from visions.relations import IdentityRelation
from visions.types.measurement_level import Nominal


class Ordinal(VisionsBaseType):
    @classmethod
    def get_relations(cls):
        return [IdentityRelation(Ordinal, Nominal)]

    @classmethod
    def contains_op(cls, series: pd.Series) -> bool:
        return not (pdt.is_categorical_dtype(series) and not series.cat.ordered)

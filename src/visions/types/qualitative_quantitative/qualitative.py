import pandas as pd
import pandas.core.dtypes.common as pdt

from visions import Generic, VisionsBaseType
from visions.relations import IdentityRelation


class Qualitative(VisionsBaseType):
    @classmethod
    def get_relations(cls):
        return [IdentityRelation(Qualitative, Generic)]

    @classmethod
    def contains_op(cls, series: pd.Series) -> bool:
        return (
            pdt.is_categorical_dtype(series)
            or pdt.is_string_dtype(series)
            or pdt.is_bool_dtype(series)
        )

import pandas as pd
import pandas.core.dtypes.common as pdt

from visions import Generic, VisionsBaseType
from visions.relations import IdentityRelation


class Quantitative(VisionsBaseType):
    @classmethod
    def get_relations(cls):
        return [IdentityRelation(Quantitative, Generic)]

    @classmethod
    def contains_op(cls, series: pd.Series) -> bool:
        return (
            not pdt.is_categorical_dtype(series)
            and not pdt.is_string_dtype(series)
            and not pdt.is_bool_dtype(series)
        )

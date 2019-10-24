import pandas.api.types as pdt
import pandas as pd

from visions.core.model.type import VisionsBaseType


class visions_boolean(VisionsBaseType):
    """**Boolean** implementation of :class:`visions.core.models.VisionsBaseType`.

    Examples:
        >>> x = pd.Series([True, False, None])
        >>> x in visions_boolean
        True
    """

    @classmethod
    def contains_op(cls, series: pd.Series) -> bool:
        return pdt.is_bool_dtype(series) or series.dtype == "Bool"

    @classmethod
    def cast_op(cls, series: pd.Series, operation=None) -> pd.Series:
        try:
            return series.astype(bool)
        except ValueError:
            return pd.to_numeric(series).astype("Bool")

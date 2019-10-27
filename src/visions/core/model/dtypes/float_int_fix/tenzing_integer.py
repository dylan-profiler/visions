import pandas.api.types as pdt
import pandas as pd

from visions.core.model.type import VisionsBaseType


class visions_integer(VisionsBaseType):
    """**Integer** implementation of :class:`visions.core.models.VisionsBaseType`.

    Examples:
        >>> x = pd.Series([1, 2, 3])
        >>> x in visions_integer
        True
    """

    @classmethod
    def contains_op(cls, series: pd.Series) -> bool:
        return pdt.is_integer_dtype(series)

    @classmethod
    def cast_op(cls, series: pd.Series, operation=None) -> pd.Series:
        try:
            return series.astype(int)
        except ValueError:
            return series.astype("Int64")

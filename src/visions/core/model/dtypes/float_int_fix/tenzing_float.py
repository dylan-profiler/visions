import pandas.api.types as pdt
import numpy as np
import pandas as pd

from visions.core.model.type import VisionsBaseType


class visions_float(VisionsBaseType):
    """**Float** implementation of :class:`visions.core.models.VisionsBaseType`.
    >>> x = pd.Series([1.0, 2.5, 5.0, np.nan])
    >>> x in visions_float
    True
    """

    @classmethod
    def contains_op(cls, series: pd.Series) -> bool:
        return pdt.is_float_dtype(series)

    @classmethod
    def cast_op(cls, series: pd.Series, operation=None) -> bool:
        return series.astype(float)

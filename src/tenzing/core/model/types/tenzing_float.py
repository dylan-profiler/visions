import pandas.api.types as pdt
import numpy as np
import pandas as pd

from tenzing.core.model.types.tenzing_generic import tenzing_generic
from tenzing.core.model.types.tenzing_integer import tenzing_integer


class tenzing_float(tenzing_generic):
    """**Float** implementation of :class:`tenzing.core.models.tenzing_model`.

    Examples:
        >>> x = pd.Series([1.0, 2.5, 5.0, np.nan])
        >>> x in tenzing_float
        True
    """

    @classmethod
    def mask(cls, series: pd.Series) -> pd.Series:
        super_mask = super().mask(series)
        if not pdt.is_float_dtype(series):
            mask = series[super_mask].apply(lambda _: False)
        elif series in tenzing_integer:
            mask = series[super_mask].apply(lambda _: False)
        else:
            mask = series[super_mask].apply(lambda _: True)

        return super_mask & mask

    @classmethod
    def cast_op(cls, series: pd.Series, operation=None) -> bool:
        return series.astype(float)

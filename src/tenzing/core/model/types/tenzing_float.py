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
        if not pdt.is_float_dtype(series):
            return series.apply(lambda _: False)

        return series.notna() & (np.isfinite(series))

    @classmethod
    def cast_op(cls, series: pd.Series, operation=None) -> bool:
        return series.astype(float)

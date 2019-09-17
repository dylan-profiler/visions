import pandas as pd
import numpy as np

from tenzing.core.models import tenzing_model


class infinite_generic(tenzing_model):
    """**Infinite series** implementation of :class:`tenzing.core.models.tenzing_model`.

    Examples:
        >>> x = pd.Series([np.inf, np.NINF])
        >>> x in infinite_generic
        True
    """

    @classmethod
    def mask(cls, series: pd.Series) -> pd.Series:
        return (~np.isfinite(series)) & series.notnull()

    @classmethod
    def cast_op(cls, series: pd.Series, operation=None) -> pd.Series:
        series.loc[:] = np.inf
        return series

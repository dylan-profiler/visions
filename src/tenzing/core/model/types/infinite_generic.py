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
        super_mask = super().mask(series)
        return super_mask & series[super_mask].apply(
            lambda x: type(x) == float and np.isinf(x)
        )

    @classmethod
    def cast_op(cls, series: pd.Series, operation=None) -> pd.Series:
        series.loc[:] = np.inf
        return series

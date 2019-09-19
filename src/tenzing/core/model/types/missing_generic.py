import pandas as pd
import numpy as np

from tenzing.core.models import tenzing_model


class missing_generic(tenzing_model):
    """**Empty series** implementation of :class:`tenzing.core.models.tenzing_model`.

    Examples:
        >>> x = pd.Series([np.nan])
        >>> x in missing_generic
        True
    """

    @classmethod
    def mask(cls, series: pd.Series) -> pd.Series:
        super_mask = super().mask(series)
        return super_mask & series[super_mask].isna()

    @classmethod
    def cast_op(cls, series: pd.Series, operation=None) -> pd.Series:
        series.loc[:] = np.nan
        return series

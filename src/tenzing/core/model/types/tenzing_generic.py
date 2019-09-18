import numpy as np
import pandas as pd
from tenzing.core.models import tenzing_model

import pandas.api.types as pdt


class tenzing_generic(tenzing_model):
    """**Generic** implementation of :class:`tenzing.core.models.tenzing_model`.

    Examples:
        >>> x = pd.Series(['a', 1, np.nan])
        >>> x in tenzing_generic
        True
    """

    @classmethod
    def mask(cls, series: pd.Series) -> pd.Series:
        super_mask = super().mask(series)

        mask = series[super_mask].notna()
        if pdt.is_float_dtype(series[super_mask]):
            mask &= np.isfinite(series[super_mask])
        # TODO: series.empty == strict
        return super_mask & mask

    @classmethod
    def cast_op(cls, series: pd.Series) -> pd.Series:
        return series

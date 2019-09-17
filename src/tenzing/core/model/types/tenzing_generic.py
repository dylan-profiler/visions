import numpy as np
import pandas as pd
from tenzing.core.models import tenzing_model


class tenzing_generic(tenzing_model):
    """**Generic** implementation of :class:`tenzing.core.models.tenzing_model`.

    Examples:
        >>> x = pd.Series(['a', 1, np.nan])
        >>> x in tenzing_generic
        True
    """

    @classmethod
    def mask(cls, series: pd.Series) -> pd.Series:
        # TODO: exclude inf
        # if (~np.isfinite(series)).any():
        #     return False
        # TODO: series.empty == strict
        return series.notna()

    @classmethod
    def contains_op(cls, series: pd.Series) -> bool:
        if not super().contains_op(series):
            return False

        return cls.mask(series).all()

    @classmethod
    def cast_op(cls, series: pd.Series) -> pd.Series:
        return series

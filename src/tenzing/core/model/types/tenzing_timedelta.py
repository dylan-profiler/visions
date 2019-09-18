import pandas.api.types as pdt
import pandas as pd
import numpy as np
from pandas._libs.tslibs.timedeltas import Timedelta

from tenzing.core.model.types.tenzing_generic import tenzing_generic


class tenzing_timedelta(tenzing_generic):
    """**Timedelta** implementation of :class:`tenzing.core.models.tenzing_model`.

    Examples:
        >>> x = pd.Series([pd.Timedelta(days=i) for i in range(3)])
        >>> x in tenzing_timedelta
        True
    """

    @classmethod
    def mask(cls, series: pd.Series) -> pd.Series:
        super_mask = super().mask(series)
        return super_mask & series[super_mask].apply(
            lambda x: issubclass(type(x), np.timedelta64) or isinstance(x, Timedelta)
        )

    @classmethod
    def cast_op(cls, series: pd.Series, operation=None) -> pd.Series:
        return pd.to_timedelta(series)

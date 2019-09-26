import pandas.api.types as pdt
import pandas as pd
import numpy as np
from pandas._libs.tslibs.timedeltas import Timedelta

from tenzing.core.models import tenzing_model


class tenzing_timedelta(tenzing_model):
    """**Timedelta** implementation of :class:`tenzing.core.models.tenzing_model`.
    >>> x = pd.Series([pd.Timedelta(days=i) for i in range(3)])
    >>> x in tenzing_timedelta
    True
    """

    @classmethod
    def contains_op(cls, series: pd.Series) -> bool:
        return pdt.is_timedelta64_dtype(series)

    @classmethod
    def cast_op(cls, series: pd.Series, operation=None) -> pd.Series:
        return pd.to_timedelta(series)

import pandas.api.types as pdt
from pandas._libs.tslibs.timestamps import Timestamp
import pandas as pd
import numpy as np
from tenzing.core.models import tenzing_model


class tenzing_datetime(tenzing_model):
    """**Datetime** implementation of :class:`tenzing.core.models.tenzing_model`.
    >>> x = pd.Series([pd.datetime(2017, 3, 5), pd.datetime(2019, 12, 4)])
    >>> x in tenzing_datetime
    True
    """

    @classmethod
    def contains_op(cls, series: pd.Series) -> bool:
        return series.apply(
            lambda x: issubclass(type(x), np.datetime64) or isinstance(x, Timestamp)
        ).all()

    @classmethod
    def cast_op(cls, series: pd.Series, operation=None) -> pd.Series:
        return pd.to_datetime(series)

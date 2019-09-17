import pandas.api.types as pdt
import pandas as pd
import numpy as np
from pandas._libs.tslibs.timestamps import Timestamp

from tenzing.core.model.types.tenzing_generic import tenzing_generic


class tenzing_datetime(tenzing_generic):
    """**Datetime** implementation of :class:`tenzing.core.models.tenzing_model`.

    Examples:
        >>> x = pd.Series([pd.datetime(2017, 3, 5), pd.datetime(2019, 12, 4)])
        >>> x in tenzing_datetime
        True
    """

    @classmethod
    def mask(cls, series: pd.Series) -> pd.Series:
        # if pdt.is_datetime64_any_dtype(series):
        #     return series.apply(lambda _: True)

        return series.apply(lambda x: issubclass(type(x), np.datetime64) or isinstance(x, Timestamp))

    @classmethod
    def cast_op(cls, series: pd.Series, operation=None) -> pd.Series:
        return pd.to_datetime(series)

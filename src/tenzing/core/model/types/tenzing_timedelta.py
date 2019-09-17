import pandas.api.types as pdt
import pandas as pd
import numpy as np

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
        return series.apply(lambda x: issubclass(type(x), np.timedelta64))

    @classmethod
    def cast_op(cls, series: pd.Series, operation=None) -> pd.Series:
        return pd.to_timedelta(series)

import pandas.api.types as pdt
import numpy as np
import pandas as pd

from tenzing.core.model.models import tenzing_model


class tenzing_float(tenzing_model):
    """**Float** implementation of :class:`tenzing.core.models.tenzing_model`.
    >>> x = pd.Series([1.0, 2.5, 5.0, np.nan])
    >>> x in tenzing_float
    True
    """

    @classmethod
    def contains_op(cls, series: pd.Series) -> bool:
        return pdt.is_float_dtype(series)

    @classmethod
    def cast_op(cls, series: pd.Series, operation=None) -> bool:
        return series.astype(float)

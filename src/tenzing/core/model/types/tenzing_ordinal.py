import pandas.api.types as pdt
import pandas as pd
import numpy as np

from tenzing.core.model.models import tenzing_model


class tenzing_ordinal(tenzing_model):
    """**Ordinal** implementation of :class:`tenzing.core.models.tenzing_model`.
    >>> x = pd.Series([1, 2, 3, 1, 1], dtype='category')
    >>> x in tenzing_ordinal
    True
    """

    @classmethod
    def contains_op(cls, series: pd.Series) -> bool:
        return pdt.is_categorical_dtype(series) & series.applymap(np.isreal).all()

    @classmethod
    def cast_op(cls, series: pd.Series, operation=None) -> pd.Series:
        return series.astype("category")

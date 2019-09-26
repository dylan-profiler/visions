import pandas.api.types as pdt
import pandas as pd

from tenzing.core.models import tenzing_model


class tenzing_categorical(tenzing_model):
    """**Categorical** implementation of :class:`tenzing.core.models.tenzing_model`.
    >>> x = pd.Series([True, False, 1], dtype='category')
    >>> x in tenzing_categorical
    True
    """

    @classmethod
    def contains_op(cls, series: pd.Series) -> bool:
        return pdt.is_categorical_dtype(series)

    @classmethod
    def cast_op(cls, series: pd.Series, operation=None) -> pd.Series:
        return series.astype("category")

import pandas.api.types as pdt
import pandas as pd

from tenzing.core.model.models import tenzing_model


class tenzing_bool(tenzing_model):
    """**Boolean** implementation of :class:`tenzing.core.models.tenzing_model`.
    >>> x = pd.Series([True, False])
    >>> x in tenzing_bool
    True
    """

    @classmethod
    def contains_op(cls, series: pd.Series) -> bool:
        if pdt.is_categorical_dtype(series):
            return False
        elif pdt.is_object_dtype(series):
            series = series.astype('bool')

        return pdt.is_bool_dtype(series)

    @classmethod
    def cast_op(cls, series: pd.Series, operation=None) -> pd.Series:
        return series.astype(bool)

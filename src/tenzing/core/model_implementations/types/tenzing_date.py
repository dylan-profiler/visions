import pandas.api.types as pdt
import pandas as pd

from tenzing.core.model_implementations.types.tenzing_datetime import tenzing_datetime
from tenzing.utils import singleton


# @singleton.singleton_object
class tenzing_date(tenzing_datetime):
    """**Date** implementation of :class:`tenzing.core.models.tenzing_model`.

    >>> x = pd.Series([pd.datetime(2017, 3, 5), pd.datetime(2019, 12, 4)])
    >>> x in tenzing_date
    True
    """
    def contains_op(self, series):
        return pdt.is_datetime64_any_dtype(series) and series.eq(series.replace(hour=0, minute=0, second=0))

    def cast_op(self, series):
        return pd.to_datetime(series)

    def summarization_op(self, series):
        summary = super().summarization_op(series)
        # TODO: specify format
        return summary

import pandas.api.types as pdt
import pandas as pd

from tenzing.core import tenzing_model
from tenzing.core.reuse import base_summary
from tenzing.core.mixins import optionMixin
from tenzing.utils import singleton


@singleton.singleton_object
class tenzing_timedelta(optionMixin, tenzing_model):
    """**Timedelta** implementation of :class:`tenzing.core.models.tenzing_model`.

    >>> x = pd.Series([pd.Timedelta(days=i) for i in range(3)])
    >>> x in tenzing_timedelta
    True
    """
    def contains_op(self, series):
        return pdt.is_timedelta64_dtype(series)

    def cast_op(self, series):
        return pd.to_timedelta(series)

    @base_summary
    def summarization_op(self, series):
        summary = super().summarization_op(series)
        # TODO: statistics
        return summary

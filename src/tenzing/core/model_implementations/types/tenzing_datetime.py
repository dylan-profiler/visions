import pandas.api.types as pdt
import pandas as pd

from tenzing.core.mixins import optionMixin
from tenzing.core.model_implementations.types.tenzing_generic import tenzing_generic
from tenzing.core.reuse import unique_summary
from tenzing.utils import singleton


# @singleton.singleton_object
class tenzing_datetime(optionMixin, tenzing_generic):
    """**Datetime** implementation of :class:`tenzing.core.models.tenzing_model`.

    >>> x = pd.Series([pd.datetime(2017, 3, 5), pd.datetime(2019, 12, 4)])
    >>> x in tenzing_datetime
    True
    """
    def contains_op(self, series):
        return pdt.is_datetime64_any_dtype(series)

    def cast_op(self, series):
        return pd.to_datetime(series)

    @unique_summary
    def summarization_op(self, series):
        summary = super().summarization_op(series)

        aggregates = ['min', 'max']
        summary.update(series.agg(aggregates).to_dict())

        summary['range'] = summary['max'] - summary['min']
        # TODO: restrict to histogram calculation
        # summary['image'] = plotting.save_plot_to_str(series.hist())

        return summary

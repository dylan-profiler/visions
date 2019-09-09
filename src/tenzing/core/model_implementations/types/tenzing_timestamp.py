import pandas.api.types as pdt
import pandas as pd

from tenzing.core import tenzing_model
from tenzing.core.mixins.option_mixin import optionMixin
from tenzing.utils import singleton


@singleton.singleton_object
class tenzing_timestamp(optionMixin, tenzing_model):
    """**Timestamp** implementation of :class:`tenzing.core.models.tenzing_model`.

    >>> x = pd.Series([pd.datetime(2017, 3, 5), pd.datetime(2019, 12, 4)])
    >>> x in tenzing_timestamp
    True
    """
    def contains_op(self, series):
        return pdt.is_datetime64_any_dtype(series)

    def cast_op(self, series):
        return pd.to_datetime(series)

    def summarization_op(self, series):
        aggregates = ['nunique', 'min', 'max']
        summary = series.agg(aggregates).to_dict()

        summary['n_records'] = series.shape[0]
        summary['perc_unique'] = summary['nunique'] / summary['n_records']

        summary['range'] = summary['max'] - summary['min']
        # TODO: restrict to histogram calculation
        # summary['image'] = plotting.save_plot_to_str(series.hist())
        summary['memory_size'] = series.memory_usage(index=True, deep=True),

        return summary

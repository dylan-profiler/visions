import pandas.api.types as pdt

from tenzing.core import tenzing_model
from tenzing.core.mixins.option_mixin import optionMixin
from tenzing.utils import singleton


@singleton.singleton_object
class tenzing_string(optionMixin, tenzing_model):
    """**String** implementation of :class:`tenzing.core.models.tenzing_model`.

    >>> x = pd.Series(['a', 'b', np.nan])
    >>> x in tenzing_string
    True
    """
    def contains_op(self, series):
        if not pdt.is_object_dtype(series):
            return False

        return series.eq(series.astype(str)).all()

    def cast_op(self, series):
        return series.astype(str)

    def summarization_op(self, series):
        summary = series.agg(['nunique']).to_dict()
        summary['n_records'] = series.shape[0]
        summary['frequencies'] = series.value_counts().to_dict()
        summary['memory_size'] = series.memory_usage(index=True, deep=True),

        # TODO: add distribution of string lengths

        return summary

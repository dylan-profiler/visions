import pandas.api.types as pdt

from tenzing.core import tenzing_model
from tenzing.core.mixins.option_mixin import optionMixin
from tenzing.utils import singleton


@singleton.singleton_object
class tenzing_object(optionMixin, tenzing_model):
    """**Object** implementation of :class:`tenzing.core.models.tenzing_model`.

    >>> x = pd.Series(['a', 1, np.nan])
    >>> x in tenzing_object
    True
    """
    def contains_op(self, series):
        return pdt.is_object_dtype(series)

    def cast_op(self, series):
        return series.astype('object'),

    def summarization_op(self, series):
        summary = {}
        try:
            summary['nunique'] = series.nunique()
            summary['frequencies'] = series.value_counts().to_dict()
        except Exception:
            pass

        summary['n_records'] = series.shape[0]
        return summary

import pandas.api.types as pdt

from tenzing.core import tenzing_model
from tenzing.core.mixins.option_mixin import optionMixin
from tenzing.core.model_implementations.types.tenzing_integer import tenzing_integer
from tenzing.utils import singleton


@singleton.singleton_object
class tenzing_float(optionMixin, tenzing_model):
    """**Float** implementation of :class:`tenzing.core.models.tenzing_model`.

    >>> x = pd.Series([1.0, 2.5, 5.0, np.nan])
    >>> x in tenzing_float
    True
    """
    def contains_op(self, series):
        if not pdt.is_float_dtype(series):
            return False
        # TODO: are we sure we want this to depend on integer?
        elif series in tenzing_integer:
            return False
        else:
            return True

    def cast_op(self, series):
        return series.astype(float)

    def summarization_op(self, series):
        aggregates = ['nunique', 'mean', 'std', 'max', 'min', 'median']
        summary = series.agg(aggregates).to_dict()
        summary['n_records'] = series.shape[0]

        summary['n_zeros'] = (series == 0).sum()
        summary['perc_zeros'] = summary['n_zeros'] / summary['n_records']
        # summary['image'] = plotting.histogram(series)
        return summary

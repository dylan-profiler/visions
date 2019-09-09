import pandas.api.types as pdt

from tenzing.core import tenzing_model
from tenzing.core.mixins.option_mixin import optionMixin
from tenzing.utils import singleton


@singleton.singleton_object
class tenzing_integer(optionMixin, tenzing_model):
    """**Integer** implementation of :class:`tenzing.core.models.tenzing_model`.

    >>> x = pd.Series([1, 2, 3, np.nan])
    >>> x in tenzing_integer
    True
    """
    def contains_op(self, series):
        if pdt.is_integer_dtype(series):
            return True
        elif pdt.is_float_dtype(series):
            # Need this additional check because it's an Option[Int] which in
            # pandas land will result in integers with decimal trailing 0's
            return series.eq(series.astype(int)).all()
        else:
            return False

    def cast_op(self, series):
        return series.astype(int)

    def summarization_op(self, series):
        aggregates = ['nunique', 'mean', 'std', 'max', 'min', 'median']
        summary = series.agg(aggregates).to_dict()
        summary['n_records'] = series.shape[0]

        summary['n_zeros'] = (series == 0).sum()
        summary['perc_zeros'] = summary['n_zeros'] / summary['n_records']

        # summary['image'] = plotting.histogram(series)
        return summary

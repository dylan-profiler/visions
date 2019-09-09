import pandas.api.types as pdt
import numpy as np

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
        aggregates = ['nunique', 'median', "mean", "std", "var", "min", "max", "kurt", "skew", "sum", "mad"]
        summary = series.agg(aggregates).to_dict()

        quantiles = [0.05, 0.25, 0.5, 0.75, 0.95]
        for percentile, value in series.quantile(quantiles).to_dict().items():
            summary["quantile_{:d}".format(int(percentile * 100))] = value

        summary["range"] = summary["max"] - summary["min"]
        summary["iqr"] = summary["quantile_75"] - summary["quantile_25"]
        summary["cv"] = summary["std"] / summary["mean"] if summary["mean"] else np.NaN

        summary['n_records'] = series.shape[0]

        summary['n_zeros'] = (series == 0).sum()
        summary['perc_zeros'] = summary['n_zeros'] / summary['n_records']

        # summary['image'] = plotting.histogram(series)
        return summary

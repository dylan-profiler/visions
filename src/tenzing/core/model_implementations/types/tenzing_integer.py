import pandas.api.types as pdt
import numpy as np

from tenzing.core.mixins import optionMixin, infMixin
from tenzing.core.model_implementations.types.tenzing_generic import tenzing_generic
from tenzing.core.reuse import unique_summary, zero_summary
from tenzing.utils import singleton


# @singleton.singleton_object
class tenzing_integer(optionMixin, infMixin, tenzing_generic):
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
        # TODO: split in NaN
        return series.astype(int)

    @zero_summary
    @unique_summary
    def summarization_op(self, series):
        summary = super().summarization_op(series)
        aggregates = [
            "median",
            "mean",
            "std",
            "var",
            "min",
            "max",
            "kurt",
            "skew",
            "sum",
            "mad",
        ]
        summary.update(series.agg(aggregates).to_dict())

        quantiles = [0.05, 0.25, 0.5, 0.75, 0.95]
        for percentile, value in series.quantile(quantiles).to_dict().items():
            summary["quantile_{:d}".format(int(percentile * 100))] = value

        summary["range"] = summary["max"] - summary["min"]
        summary["iqr"] = summary["quantile_75"] - summary["quantile_25"]
        summary["cv"] = summary["std"] / summary["mean"] if summary["mean"] else np.NaN

        # summary['image'] = plotting.histogram(series)
        return summary

import pandas.api.types as pdt
import numpy as np

from tenzing.core.model_implementations.types.tenzing_generic import tenzing_generic
from tenzing.core.reuse import unique_summary, zero_summary


class tenzing_integer(tenzing_generic):
    """**Integer** implementation of :class:`tenzing.core.models.tenzing_model`.

    >>> x = pd.Series([1, 2, 3, np.nan])
    >>> x in tenzing_integer
    True
    """

    @classmethod
    def contains_op(cls, series):
        if pdt.is_integer_dtype(series) and not series.hasnans:
            return True
        elif pdt.is_float_dtype(series):
            # Need this additional check because it's an Option[Int] which in
            # pandas land will result in integers with decimal trailing 0's
            try:
                return series.eq(series.astype(int)).all()
            except ValueError:
                return False
        else:
            return False

    @classmethod
    def cast_op(cls, series, operation=None):
        # TODO: split in NaN
        xseries = cls.get_series(series)
        return xseries.astype(int)

    @classmethod
    def summarize_entry(cls, series):
        mseries = super().get_series(series)
        summary = super().summarization_op(series)
        summary.update(cls.summarization_op(mseries))
        return summary

    @classmethod
    @unique_summary
    @zero_summary
    def summarization_op(cls, series):
        summary = super().summarization_op(series)
        summary = {}
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

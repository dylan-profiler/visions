import pandas.api.types as pdt

from tenzing.core.model_implementations.types.tenzing_generic import tenzing_generic
from tenzing.core.reuse import unique_summary, zero_summary


class tenzing_complex(tenzing_generic):
    """**Complex** implementation of :class:`tenzing.core.models.tenzing_model`.

    >>> x = pd.Series([np.complex(0, 0), np.complex(1, 2), np.complex(3, -1), np.nan])
    >>> x in tenzing_complex
    True
    """

    @classmethod
    def contains_op(cls, series):
        return pdt.is_complex_dtype(series)

    @classmethod
    def cast_op(cls, series, operation=None):
        return series.astype("complex")

    @classmethod
    @unique_summary
    @zero_summary
    def summarization_op(cls, series):
        summary = super().summarization_op(series)

        aggregates = ["mean", "std", "var", "min", "max", "sum"]

        summary.update(series.agg(aggregates).to_dict())

        # TODO: cleaner way of doing this
        summary["scatter_data"] = series.to_numpy()
        return summary

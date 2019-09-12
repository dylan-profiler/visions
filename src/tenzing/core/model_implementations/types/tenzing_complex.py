import pandas.api.types as pdt

from tenzing.core.mixins import optionMixin
from tenzing.core.model_implementations.types.tenzing_generic import tenzing_generic
from tenzing.core.reuse import unique_summary, zero_summary
from tenzing.utils import singleton


# @singleton.singleton_object
class tenzing_complex(optionMixin, tenzing_generic):
    """**Complex** implementation of :class:`tenzing.core.models.tenzing_model`.

    >>> x = pd.Series([np.complex(0, 0), np.complex(1, 2), np.complex(3, -1), np.nan])
    >>> x in tenzing_complex
    True
    """
    def contains_op(self, series):
        return pdt.is_complex_dtype(series)

    def cast_op(self, series):
        return series.astype('complex')

    @unique_summary
    @zero_summary
    def summarization_op(self, series):
        summary = super().summarization_op(series)

        aggregates = ["mean", "std", "var", "min", "max", "sum"]

        summary.update(series.agg(aggregates).to_dict())

        # TODO: cleaner way of doing this
        summary["scatter_data"] = series.to_numpy()
        return summary

import pandas.api.types as pdt

from tenzing.core.model_implementations.types.tenzing_generic import tenzing_generic
from tenzing.core.reuse import unique_summary, base_summary


class tenzing_object(tenzing_generic):
    """**Object** implementation of :class:`tenzing.core.models.tenzing_model`.

    >>> x = pd.Series(['a', 1, np.nan])
    >>> x in tenzing_object
    True
    """

    @classmethod
    def contains_op(cls, series):
        return pdt.is_object_dtype(series)

    @classmethod
    def cast_op(cls, series, operation=None):
        return series.astype("object")

    @classmethod
    @base_summary
    @unique_summary
    def summarization_op(cls, series):
        summary = super().summarization_op(series)

        # summary = {}
        # try:
        #     summary['nunique'] = series.nunique()
        #     summary['frequencies'] = series.value_counts().to_dict()
        # except Exception:
        #     pass

        return summary

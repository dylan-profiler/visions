import pandas.api.types as pdt

from tenzing.core.model_implementations.types.tenzing_generic import tenzing_generic
from tenzing.core.reuse import unique_summary


class tenzing_object(tenzing_generic):
    """**Object** implementation of :class:`tenzing.core.models.tenzing_model`.

    >>> x = pd.Series(['a', 1, np.nan])
    >>> x in tenzing_object
    True
    """

    @classmethod
    def contains_op(cls, series):
        from tenzing.core.model_implementations.types.tenzing_string import tenzing_string
        # TODO: find better way of excluding subclasses
        from tenzing.core.model_implementations.types.tenzing_float import tenzing_float
        return pdt.is_object_dtype(series) and not series in tenzing_string and not series in tenzing_float

    @classmethod
    def cast_op(cls, series, operation=None):
        return series.astype("object")

    @classmethod
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

import pandas.api.types as pdt

from tenzing.core.model_implementations import tenzing_generic
from tenzing.core.reuse import unique_summary


class tenzing_categorical(tenzing_generic):
    """**Categorical** implementation of :class:`tenzing.core.models.tenzing_model`.

    >>> x = pd.Series([True, False, 1], dtype='category')
    >>> x in tenzing_categorical
    True
    """

    @classmethod
    def contains_op(cls, series):
        return pdt.is_categorical_dtype(series)

    @classmethod
    def cast_op(cls, series, operation=None):
        return series.astype("category")

    @classmethod
    @unique_summary
    def summarization_op(cls, series):
        summary = super().summarization_op(series)
        summary["category_size"] = len(series.dtype._categories)
        summary["missing_categorical_values"] = (
            True if series.nunique() != summary["category_size"] else False
        )
        return summary

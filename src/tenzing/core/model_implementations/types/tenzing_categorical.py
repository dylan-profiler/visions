import pandas.api.types as pdt

from tenzing.core.mixins import optionMixin
from tenzing.core.model_implementations import tenzing_generic
from tenzing.core.reuse import unique_summary
from tenzing.utils import singleton


# @singleton.singleton_object
class tenzing_categorical(optionMixin, tenzing_generic):
    """**Categorical** implementation of :class:`tenzing.core.models.tenzing_model`.

    >>> x = pd.Series([True, False, 1], dtype='category')
    >>> x in tenzing_categorical
    True
    """
    def contains_op(self, series):
        return pdt.is_categorical_dtype(series)

    def cast_op(self, series):
        return series.astype('category')

    @unique_summary
    def summarization_op(self, series):
        summary = super().summarization_op(series)
        summary['category_size'] = len(series.dtype._categories)
        summary['missing_categorical_values'] = True if summary['n_unique'] != summary['category_size'] else False
        return summary

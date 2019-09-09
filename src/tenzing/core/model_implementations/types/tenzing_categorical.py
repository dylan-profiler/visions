import pandas.api.types as pdt

from tenzing.core import tenzing_model
from tenzing.core.mixins.option_mixin import optionMixin
from tenzing.utils import singleton


@singleton.singleton_object
class tenzing_categorical(optionMixin, tenzing_model):
    """**Categorical** implementation of :class:`tenzing.core.models.tenzing_model`.

    >>> x = pd.Series([True, False, 1], dtype='category')
    >>> x in tenzing_categorical
    True
    """
    def contains_op(self, series):
        return pdt.is_categorical_dtype(series)

    def cast_op(self, series):
        return series.astype('category')

    def summarization_op(self, series):
        # TODO: unique summary
        aggregates = ['nunique']
        summary = series.agg(aggregates).to_dict()

        # TODO: common summary
        summary['frequencies'] = series.value_counts().to_dict()

        summary['category_size'] = len(series.dtype._categories)
        summary['missing_categorical_values'] = True if summary['nunique'] != summary['category_size'] else False
        return summary
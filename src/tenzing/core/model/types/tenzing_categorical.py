import pandas.api.types as pdt

from tenzing.core.model.types.tenzing_generic import tenzing_generic


class tenzing_categorical(tenzing_generic):
    # unique_summary, category_summary
    """**Categorical** implementation of :class:`tenzing.core.models.tenzing_model`.

    >>> x = pd.Series([True, False, 1], dtype='category')
    >>> x in tenzing_categorical
    True
    """

    @classmethod
    def contains_op(cls, series):
        return not series.empty and pdt.is_categorical_dtype(series)

    @classmethod
    def cast_op(cls, series, operation=None):
        return series.astype("category")

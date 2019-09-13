import numpy as np

from tenzing.core import tenzing_model


class tenzing_generic(tenzing_model):
    """**Generic** implementation of :class:`tenzing.core.models.tenzing_model`.

    >>> x = pd.Series(['a', 1, np.nan])
    >>> x in tenzing_generic
    True
    """
    @staticmethod
    def get_series_mask(series):
        return super().get_series_mask(series)

    @classmethod
    def contains_op(cls, series):
        return True

    @classmethod
    def cast_op(cls, series):
        return series

    @classmethod
    def summarization_op(cls, series):
        print('tenzing_generic.summarization_op')
        summary = super().summarization_op(series)
        return summary

import numpy as np

from tenzing.core import tenzing_model
from tenzing.utils import singleton
from tenzing.core.reuse import base_summary


# @singleton.singleton_object
class tenzing_generic(tenzing_model):
    """**Generic** implementation of :class:`tenzing.core.models.tenzing_model`.

    >>> x = pd.Series(['a', 1, np.nan])
    >>> x in tenzing_generic
    True
    """

    def contains_op(self, series):
        return True

    def cast_op(self, series):
        return series

    @base_summary
    def summarization_op(self, series):
        summary = super().summarization_op(series)
        return summary

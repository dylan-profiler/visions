import pandas.api.types as pdt
<<<<<<< HEAD

from tenzing.core import tenzing_model
from tenzing.core.reuse import base_summary
from tenzing.utils import singleton


# @singleton.singleton_object
class tenzing_generic(tenzing_model):
    """**Generic** implementation of :class:`tenzing.core.models.tenzing_model`.

    >>> x = pd.Series(['a', 1, np.nan])
    >>> x in tenzing_generic
    True
=======
import numpy as np

from tenzing.core import tenzing_model
from tenzing.core.mixins import optionMixin
from tenzing.core.reuse import unique_summary, base_summary, zero_summary
from tenzing.core.model_implementations.types.tenzing_integer import tenzing_integer
from tenzing.utils import singleton


@singleton.singleton_object
class tenzing_generic(tenzing_model):
    """**Generic** implementation of :class:`tenzing.core.models.tenzing_model`.

>>>>>>> 96b4ce43c63c9a730d9bf34a97e6780f7bbd851c
    """
    def contains_op(self, series):
        return True

    def cast_op(self, series):
<<<<<<< HEAD
        return series,

    @base_summary
    def summarization_op(self, series):
        summary = super().summarization_op(series)
        return summary
=======
        return series

    def summarization_op(self, series):
        return {}
>>>>>>> 96b4ce43c63c9a730d9bf34a97e6780f7bbd851c

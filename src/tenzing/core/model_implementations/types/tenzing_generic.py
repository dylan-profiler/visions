import pandas.api.types as pdt
import numpy as np

from tenzing.core import tenzing_model
from tenzing.core.mixins import optionMixin
from tenzing.core.reuse import unique_summary, base_summary, zero_summary
from tenzing.core.model_implementations.types.tenzing_integer import tenzing_integer
from tenzing.utils import singleton


@singleton.singleton_object
class tenzing_generic(tenzing_model):
    """**Generic** implementation of :class:`tenzing.core.models.tenzing_model`.

    """
    def contains_op(self, series):
        return True

    def cast_op(self, series):
        return series

    def summarization_op(self, series):
        return {}

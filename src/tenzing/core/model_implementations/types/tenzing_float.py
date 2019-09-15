import pandas.api.types as pdt
import numpy as np

from tenzing.core.model_implementations.types.tenzing_generic import tenzing_generic
from tenzing.core.model_implementations.types.tenzing_integer import tenzing_integer


class tenzing_float(tenzing_generic):
    """**Float** implementation of :class:`tenzing.core.models.tenzing_model`.

    >>> x = pd.Series([1.0, 2.5, 5.0, np.nan])
    >>> x in tenzing_float
    True
    """

    @classmethod
    def contains_op(cls, series):
        if series.empty:
            return False
        if not pdt.is_float_dtype(series):
            return False

        if (~np.isfinite(series)).any():
            return False
        # TODO: are we sure we want this to depend on integer?
        # I don't like it but I was worried about the integer implementation changing
        elif series in tenzing_integer:
            return False
        else:
            return True

    @classmethod
    def cast_op(cls, series, operation=None):
        return series.astype(float)

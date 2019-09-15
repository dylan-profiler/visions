import pandas.api.types as pdt
import numpy as np

from tenzing.core.model_implementations.types.tenzing_generic import tenzing_generic


class tenzing_integer(tenzing_generic):
    """**Integer** implementation of :class:`tenzing.core.models.tenzing_model`.

    >>> x = pd.Series([1, 2, 3, np.nan])
    >>> x in tenzing_integer
    True
    """

    @classmethod
    def contains_op(cls, series):
        if series.empty:
            return False

        if pdt.is_integer_dtype(series) and not series.hasnans:
            return True
        elif pdt.is_float_dtype(series):
            # Need this additional check because it's an Option[Int] which in
            # pandas land will result in integers with decimal trailing 0's
            try:
                return series.eq(series.astype(int)).all()
            except ValueError:
                return False
        else:
            return False

    @classmethod
    def cast_op(cls, series, operation=None):
        return series.astype(int)

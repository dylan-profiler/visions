import pandas as pd
from tenzing.core.model_implementations.types.tenzing_generic import tenzing_generic


class tenzing_empty(tenzing_generic):
    """**Empty series** implementation of :class:`tenzing.core.models.tenzing_model`.

    >>> x = pd.Series([], dtype=bool)
    >>> x in tenzing_empty
    True
    """

    @classmethod
    def contains_op(cls, series):
        return series.empty

    @classmethod
    def cast_op(cls, series, operation=None):
        return pd.Series([], name=series.name, dtype=series.dtype)

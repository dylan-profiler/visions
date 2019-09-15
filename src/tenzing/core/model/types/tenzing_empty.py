import pandas as pd
from tenzing.core.model.types.tenzing_generic import tenzing_generic


class tenzing_empty(tenzing_generic):
    """**Empty series** implementation of :class:`tenzing.core.models.tenzing_model`.

    >>> x = pd.Series([], dtype=bool)
    >>> x in tenzing_empty
    True
    """

    @classmethod
    def contains_op(cls, series: pd.Series) -> bool:
        return series.empty

    @classmethod
    def cast_op(cls, series: pd.Series, operation=None) -> pd.Series:
        return pd.Series([], name=series.name, dtype=series.dtype)

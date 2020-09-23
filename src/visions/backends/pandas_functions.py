import numpy as np
import pandas as pd
from pandas.api import types as pdt

from visions.types.integer import float_is_int, integer_contains, to_int
from visions.utils.series_utils import (
    func_nullable_series_contains,
    series_not_empty,
    series_not_sparse,
)


@series_not_sparse
@series_not_empty
def temp_func(cls, series, state):
    return pdt.is_integer_dtype(series)


@integer_contains.register(pd.Series)
def _(sequence: pd.Series, state: dict) -> bool:
    return temp_func(_, sequence, state)


@to_int.register(pd.Series)
def _(series: pd.Series, state: dict) -> pd.Series:
    dtype = "Int64" if series.hasnans else np.int64
    return series.astype(dtype)


@float_is_int.register(pd.Series)
@func_nullable_series_contains
def _(series: pd.Series, state: dict) -> bool:
    def check_equality(series):
        try:
            if not np.isfinite(series).all():
                return False
            return series.eq(series.astype(int)).all()
        except:
            return False

    return check_equality(series)

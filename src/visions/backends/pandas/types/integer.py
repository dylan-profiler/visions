import numpy as np
import pandas as pd
from pandas.api import types as pdt

from visions.backends.pandas.series_utils import (
    series_handle_nulls,
    series_not_empty,
    series_not_sparse,
)
from visions.types.integer import float_is_int, float_to_int, integer_contains


@integer_contains.register(pd.Series)
@series_not_sparse
@series_not_empty
def _(series: pd.Series, state: dict) -> bool:
    return pdt.is_integer_dtype(series)


@float_to_int.register(pd.Series)
def _(series: pd.Series, state: dict) -> pd.Series:
    dtype = "Int64" if series.hasnans else np.int64
    return series.astype(dtype)


@float_is_int.register(pd.Series)
@series_handle_nulls
def _(series: pd.Series, state: dict) -> bool:
    def check_equality(series):
        try:
            if not np.isfinite(series).all():
                return False
            return series.eq(series.astype(int)).all()
        except:
            return False

    return check_equality(series)

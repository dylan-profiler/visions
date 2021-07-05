import numpy as np
import pandas as pd
from pandas.api import types as pdt

from visions.backends.pandas.series_utils import (
    series_handle_nulls,
    series_not_empty,
    series_not_sparse,
)
from visions.types.float import Float
from visions.types.integer import Integer


@Integer.register_relationship(Float, pd.Series)
@series_handle_nulls
def float_is_integer(series: pd.Series, state: dict) -> bool:
    def check_equality(series):
        try:
            if not np.isfinite(series).all():
                return False
            return series.eq(series.astype(int)).all()
        except (ValueError, TypeError, AttributeError):
            return False

    return check_equality(series)


@Integer.register_transformer(Float, pd.Series)
def float_to_integer(series: pd.Series, state: dict) -> pd.Series:
    dtype = "Int64" if series.hasnans else np.int64
    return series.astype(dtype)


@Integer.contains_op.register
@series_not_sparse
@series_not_empty
def integer_contains(series: pd.Series, state: dict) -> bool:
    return pdt.is_integer_dtype(series)

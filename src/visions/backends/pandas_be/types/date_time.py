from functools import partial

import pandas as pd

from pandas.api import types as pdt

from visions.backends.pandas_be import test_utils
from visions.backends.pandas_be.series_utils import (
    series_handle_nulls,
    series_not_sparse,
    series_not_empty,
)
from visions.types import DateTime, String


@DateTime.register_relationship(String, pd.Series)
@series_handle_nulls
def string_is_datetime(series: pd.Series, state: dict) -> bool:
    exceptions = [OverflowError, TypeError]

    coerced_series = test_utils.option_coercion_evaluator(
        partial(string_to_datetime, state=state), exceptions
    )(series)
    if coerced_series is None:
        return False
    else:
        return not coerced_series.dropna().empty


@DateTime.register_transformer(String, pd.Series)
def string_to_datetime(series: pd.Series, state: dict) -> pd.Series:
    return pd.to_datetime(series)


@DateTime.contains_op.register
@series_not_sparse
@series_handle_nulls
@series_not_empty
def datetime_contains(series: pd.Series, state: dict) -> bool:
    return pdt.is_datetime64_any_dtype(series)

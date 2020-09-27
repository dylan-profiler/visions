from functools import partial

import pandas as pd
from pandas.api import types as pdt

from visions.backends.pandas import test_utils
from visions.backends.pandas.series_utils import series_not_empty, series_not_sparse
from visions.types.date_time import (
    datetime_contains,
    string_is_datetime,
    string_to_datetime,
)


@datetime_contains.register(pd.Series)
@series_not_sparse
@series_not_empty
def _(series: pd.Series, state: dict) -> bool:
    return pdt.is_datetime64_any_dtype(series)


@string_is_datetime.register(pd.Series)
def _(series: pd.Series, state: dict) -> bool:
    exceptions = [OverflowError, TypeError]
    return test_utils.coercion_test(
        partial(string_to_datetime, state=state), exceptions
    )(series)


@string_to_datetime.register(pd.Series)
def _(series: pd.Series, state: dict) -> pd.Series:
    return pd.to_datetime(series)

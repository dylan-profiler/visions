from functools import partial

import pandas as pd

# from dateutil.parser import ParserError
from pandas.api import types as pdt

from visions.backends.pandas_be import test_utils
from visions.backends.pandas_be.series_utils import series_not_empty, series_not_sparse
from visions.types import DateTime, String


@DateTime.register_relationship(String, pd.Series)
def string_is_datetime(series: pd.Series, state: dict) -> bool:
    exceptions = [OverflowError, TypeError, ValueError]
    return test_utils.coercion_test(
        partial(string_to_datetime, state=state), exceptions
    )(series)


@DateTime.register_transformer(String, pd.Series)
def string_to_datetime(series: pd.Series, state: dict) -> pd.Series:
    return pd.to_datetime(series)


@DateTime.contains_op.register
@series_not_sparse
@series_not_empty
def datetime_contains(series: pd.Series, state: dict) -> bool:
    return pdt.is_datetime64_any_dtype(series)

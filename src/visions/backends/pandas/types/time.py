from datetime import date, time

import pandas as pd

from visions.backends.pandas.series_utils import (
    class_name_attrs,
    series_handle_nulls,
    series_not_empty,
)
from visions.types.time import datetime_is_time, datetime_to_time, time_contains


@datetime_is_time.register(pd.Series)
@series_handle_nulls
def _(series: pd.Series) -> bool:
    dtseries = series.dt.date
    value = date(1, 1, 1)
    return all(v == value for v in dtseries)


@datetime_to_time.register(pd.Series)
def _(series: pd.Series, state: dict) -> pd.Series:
    return series.dt.time


@time_contains.register(pd.Series)
@series_handle_nulls
@series_not_empty
def _(series: pd.Series, state: dict) -> bool:
    return class_name_attrs(series, time, ["microsecond", "hour"])

from datetime import date, time

import pandas as pd

from visions.backends.pandas.series_utils import (
    class_name_attrs,
    series_handle_nulls,
    series_not_empty,
)
from visions.types.date import Date
from visions.types.date_time import DateTime


@Date.register_relationship(DateTime, pd.Series)
@series_handle_nulls
def datetime_is_date(series: pd.Series, state: dict) -> bool:
    dtseries = series.dt.time
    value = time(0, 0)
    return all(v == value for v in dtseries)


@Date.register_transformer(DateTime, pd.Series)
def datetime_to_date(series: pd.Series, state: dict) -> pd.Series:
    return series.dt.date


@Date.contains_op.register
@series_handle_nulls
@series_not_empty
def date_contains(series: pd.Series, state: dict) -> bool:
    return class_name_attrs(series, date, ["year", "month", "day"])

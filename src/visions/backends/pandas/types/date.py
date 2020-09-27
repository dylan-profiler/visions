from datetime import date, time

import pandas as pd

from visions.backends.pandas.series_utils import (
    class_name_attrs,
    series_handle_nulls,
    series_not_empty,
)
from visions.types.date import date_contains, datetime_is_date, datetime_to_date


@datetime_is_date.register(pd.Series)
@series_handle_nulls
def _(series: pd.Series, state: dict) -> bool:
    dtseries = series.dt.time
    value = time(0, 0)
    return all(v == value for v in dtseries)


@datetime_to_date.register(pd.Series)
def _(series: pd.Series, state: dict) -> pd.Series:
    return series.dt.date


@date_contains.register(pd.Series)
@series_handle_nulls
@series_not_empty
def _(series: pd.Series, state: dict) -> bool:
    return class_name_attrs(series, date, ["year", "month", "day"])

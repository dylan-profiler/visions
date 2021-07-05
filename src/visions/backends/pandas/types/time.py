from datetime import time

import pandas as pd

from visions.backends.pandas.series_utils import (
    class_name_attrs,
    series_handle_nulls,
    series_not_empty,
)
from visions.types.time import Time

# @Time.register_relationship(DateTime, pd.Series)
# @series_handle_nulls
# def datetime_is_time(series: pd.Series) -> bool:
#     dtseries = series.dt.date
#     value = date(1, 1, 1)
#     return all(v == value for v in dtseries)
#
#
# @Time.register_transformer(DateTime, pd.Series)
# def datetime_to_time(series: pd.Series, state: dict) -> pd.Series:
#     return series.dt.time


@Time.contains_op.register
@series_handle_nulls
@series_not_empty
def time_contains(series: pd.Series, state: dict) -> bool:
    return class_name_attrs(series, time, ["microsecond", "hour"])

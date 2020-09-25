from typing import Callable, Dict, TypeVar
import functools
import pandas as pd

from visions import String
from visions.relations import InferenceRelation
from visions.utils.coercion import test_utils


T = TypeVar('T')


def redirect_state(func: Callable[[pd.Series], T]) -> Callable[[pd.Series, Dict], T]:
    @functools.wraps(func)
    def inner(series: pd.Series, state: Dict) -> T:
        return func(series)
    return inner


def to_datetime_year_week(series: pd.Series) -> pd.Series:
    """Convert a series of the format YYYY/UU (year, week) to datetime.
    A '0' is added as day dummy value, as pandas requires a day value to parse.

    Args:
        series: the Series to parse

    Returns:
        A datetime series

    Examples:
        >>> series = pd.Series(['2018/47', '2018/12', '2018/03'])
        >>> parsed_series = to_datetime_year_week(series)
        >>> print(parsed_series.dt.week)
        0    47
        1    12
        2     3
        dtype: int64
    """
    return pd.to_datetime(series + "0", format="%Y/%U%w")


def to_datetime_year_month_day(series: pd.Series) -> pd.Series:
    """Convert a series of the format YYYYMMDD (year, month, day) to datetime.

    Args:
        series: the Series to parse

    Returns:
        A datetime series

    Examples:
        >>> series = pd.Series(['20181201', '20181202', '20181203'])
        >>> parsed_series = to_datetime_year_week(series)
        >>> print(parsed_series.dt.day)
        0    1
        1    2
        2    3
        dtype: int64
    """
    return pd.to_datetime(series, format="%Y%m%d")


def _to_datetime(cls, func) -> InferenceRelation:
    return InferenceRelation(
        relationship=redirect_state(test_utils.coercion_test(func)),
        transformer=redirect_state(func),
        related_type=String,
        type=cls,
    )


def string_to_datetime_year_week(cls) -> InferenceRelation:
    return _to_datetime(cls, to_datetime_year_week)


def string_to_datetime_year_month_day(cls) -> InferenceRelation:
    return _to_datetime(cls, to_datetime_year_month_day)

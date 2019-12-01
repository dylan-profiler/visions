import pandas as pd

from visions.core.model import TypeRelation
from visions.utils.coercion import test_utils


def to_datetime_year_week(series):
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


def string_to_datetime_year_week():
    return TypeRelation(
        inferential=True,
        relationship=test_utils.coercion_test(to_datetime_year_week),
        transformer=to_datetime_year_week,
    )

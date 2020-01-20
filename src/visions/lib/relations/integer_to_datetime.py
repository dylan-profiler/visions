from visions import visions_integer, visions_datetime
from visions.core.model import TypeRelation
from visions.lib.relations.string_to_datetime import to_datetime_year_month_day
from visions.utils.coercion import test_utils
import pandas as pd


def to_datetime(series: pd.Series) -> pd.Series:
    return pd.to_datetime(series)


# TODO: do only convert obvious dates (20191003000000)
def integer_to_datetime():
    return TypeRelation(
        inferential=True,
        relationship=test_utils.coercion_test(lambda s: to_datetime(s.astype(str))),
        transformer=to_datetime,
        type=visions_datetime,
        related_type=visions_integer,
    )


def integer_to_datetime_year_month_day():
    return TypeRelation(
        inferential=True,
        relationship=test_utils.coercion_test(
            lambda s: to_datetime_year_month_day(s.astype(str))
        ),
        transformer=to_datetime,
        type=visions_datetime,
        related_type=visions_integer,
    )

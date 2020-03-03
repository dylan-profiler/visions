from visions import visions_integer
from visions.core.model.relations import InferenceRelation
from visions.lib.relations.string_to_datetime import to_datetime_year_month_day
from visions.utils.coercion import test_utils
import pandas as pd


def to_datetime(series: pd.Series) -> pd.Series:
    return pd.to_datetime(series)


def _to_datetime(cls, func):
    return InferenceRelation(
        relationship=test_utils.coercion_test(lambda s: func(s.astype(str))),
        transformer=func,
        type=cls,
        related_type=visions_integer,
    )


# TODO: do only convert obvious dates (20191003000000)
def integer_to_datetime(cls):
    return _to_datetime(cls, to_datetime)


def integer_to_datetime_year_month_day(cls):
    return _to_datetime(cls, to_datetime_year_month_day)


# Custom NaN value
# #     series[series == nan_value] = None

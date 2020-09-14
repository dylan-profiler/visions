from datetime import date, time
from typing import Optional, Sequence

import pandas as pd

from visions.relations import IdentityRelation, TypeRelation
from visions.types.type import VisionsBaseType
from visions.utils.series_utils import (
    class_name_attrs,
    func_nullable_series_contains,
    nullable_series_contains,
    series_not_empty,
)


@func_nullable_series_contains
def test_time(series: pd.Series) -> Optional[bool]:
    dtseries = series.dt.date
    value = date(1, 1, 1)
    return True if all(v == value for v in dtseries) else None


def to_time(series: pd.Series, state: dict) -> pd.Series:
    return series.dt.time


def _get_relations(cls) -> Sequence[TypeRelation]:
    from visions.types import Object

    relations = [IdentityRelation(cls, Object)]
    return relations


class Time(VisionsBaseType):
    """**Time** implementation of :class:`visions.types.type.VisionsBaseType`.

    Examples:
        >>> x = pd.Series([datetime.time(10, 8, 4), datetime.time(21, 17, 0)])
        >>> x in visions.Time
        True
    """

    @classmethod
    def get_relations(cls) -> Sequence[TypeRelation]:
        return _get_relations(cls)

    @classmethod
    @series_not_empty
    @nullable_series_contains
    def contains_op(cls, series: pd.Series, state: dict) -> bool:
        return class_name_attrs(series, time, ["microsecond", "hour"])

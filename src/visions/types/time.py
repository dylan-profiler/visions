from datetime import time, date

from typing import Sequence

import pandas as pd

from visions.relations import IdentityRelation, TypeRelation, InferenceRelation
from visions.types.type import VisionsBaseType
from visions.utils.series_utils import (
    nullable_series_contains,
    class_name_attrs,
)
from visions.utils.coercion import test_utils


def test_time(series):
    dtseries = series.copy().dropna().dt.date
    return all(v == date(1, 1, 1) for v in dtseries)


def to_time(series):
    return series.dt.time


def _get_relations(cls) -> Sequence[TypeRelation]:
    from visions.types import DateTime, Object

    relations = [
        IdentityRelation(cls, Object),
        InferenceRelation(
            cls,
            DateTime,
            relationship=test_utils.coercion_test(test_time),
            transformer=to_time,
        ),
    ]
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
    @nullable_series_contains
    def contains_op(cls, series: pd.Series) -> bool:
        return class_name_attrs(series, time, ["microsecond", "hour"])

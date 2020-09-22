from datetime import date, time
from typing import Sequence

import pandas as pd

from visions.relations import IdentityRelation, InferenceRelation, TypeRelation
from visions.types.type import VisionsBaseType
from visions.utils import func_nullable_series_contains
from visions.utils.series_utils import (
    class_name_attrs,
    nullable_series_contains,
    series_not_empty,
)


@func_nullable_series_contains
def datetime_is_date(series, state: dict):
    dtseries = series.dt.time
    value = time(0, 0)
    return True if all(v == value for v in dtseries) else None


def to_date(series, state: dict):
    return series.dt.date


def _get_relations(cls) -> Sequence[TypeRelation]:
    from visions.types import DateTime, Object

    relations = [
        IdentityRelation(cls, Object),
        InferenceRelation(
            cls,
            DateTime,
            relationship=datetime_is_date,
            transformer=to_date,
        ),
    ]
    return relations


class Date(VisionsBaseType):
    """**Date** implementation of :class:`visions.types.type.VisionsBaseType`.
    All values are should be datetime.date or missing

    Examples:
        >>> x = pd.Series([datetime.date(2017, 3, 5), datetime.date(2019, 12, 4)])
        >>> x in visions.Date
        True
    """

    @classmethod
    def get_relations(cls) -> Sequence[TypeRelation]:
        return _get_relations(cls)

    @classmethod
    @series_not_empty
    @nullable_series_contains
    def contains_op(cls, series: pd.Series, state: dict) -> bool:
        return class_name_attrs(series, date, ["year", "month", "day"])

from functools import partial
from typing import Sequence

import pandas as pd
from pandas.api import types as pdt

from visions.relations import IdentityRelation, InferenceRelation, TypeRelation
from visions.types.type import VisionsBaseType
from visions.utils.coercion import test_utils
from visions.utils.series_utils import (
    nullable_series_contains,
    series_not_empty,
    series_not_sparse,
)


def string_is_datetime(series: pd.Series, state: dict) -> bool:
    exceptions = [OverflowError, TypeError]

    coerced_series = test_utils.option_coercion_evaluator(
        partial(to_datetime, state=state), exceptions
    )(series)
    if coerced_series is None:
        return False
    else:
        return not coerced_series.dropna().empty


def to_datetime(series: pd.Series, state: dict) -> pd.Series:
    return pd.to_datetime(series)


def _get_relations(cls) -> Sequence[TypeRelation]:
    from visions.types import Generic, String

    relations = [
        IdentityRelation(cls, Generic),
        InferenceRelation(
            cls,
            String,
            relationship=string_is_datetime,
            transformer=to_datetime,
        ),
    ]
    return relations


class DateTime(VisionsBaseType):
    """**Datetime** implementation of :class:`visions.types.type.VisionsBaseType`.

    Examples:
        >>> x = pd.Series([pd.datetime(2017, 3, 5), pd.datetime(2019, 12, 4)])
        >>> x in visions.DateTime
        True
    """

    @classmethod
    def get_relations(cls) -> Sequence[TypeRelation]:
        return _get_relations(cls)

    @classmethod
    @series_not_sparse
    @nullable_series_contains
    @series_not_empty
    def contains_op(cls, series: pd.Series, state: dict) -> bool:
        return pdt.is_datetime64_any_dtype(series)

import pandas.api.types as pdt
import pandas as pd
from typing import Sequence

from visions.core.model.relations import (
    IdentityRelation,
    InferenceRelation,
)
from visions.core.model import TypeRelation
from visions.core.model.type import VisionsBaseType


def _get_relations() -> Sequence[TypeRelation]:
    from visions.core.implementations.types import visions_datetime

    relations = [IdentityRelation(visions_time, visions_datetime)]
    return relations


class visions_time(VisionsBaseType):
    """**Time** implementation of :class:`visions.core.model.type.VisionsBaseType`.

    Examples:
        >>> x = pd.Series([pd.datetime(2017, 3, 5), pd.datetime(2019, 12, 4)])
        >>> x in visions_time
        True
    """

    @classmethod
    def get_relations(cls) -> Sequence[TypeRelation]:
        return _get_relations()

    @classmethod
    def contains_op(cls, series: pd.Series) -> bool:
        if not pdt.is_datetime64_any_dtype(series):
            return False

        temp_series = series.dropna().dt

        time_val_map = {"day": 1, "month": 1, "year": 1}
        return all(
            getattr(temp_series, time_part).eq(val).all()
            for time_part, val in time_val_map.items()
        )

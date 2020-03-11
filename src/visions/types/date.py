from typing import Sequence

import pandas as pd
import pandas.api.types as pdt

from visions.relations import IdentityRelation, TypeRelation
from visions.types import VisionsBaseType


def _get_relations(cls) -> Sequence[TypeRelation]:
    from visions.types import DateTime

    relations = [IdentityRelation(cls, DateTime)]
    return relations


class Date(VisionsBaseType):
    """**Date** implementation of :class:`visions.types.type.VisionsBaseType`.

    Examples:
        >>> x = pd.Series([pd.datetime(2017, 3, 5), pd.datetime(2019, 12, 4)])
        >>> x in visions.Date
        True
    """

    @classmethod
    def get_relations(cls) -> Sequence[TypeRelation]:
        return _get_relations(cls)

    @classmethod
    def contains_op(cls, series: pd.Series) -> bool:
        if not pdt.is_datetime64_any_dtype(series):
            return False

        temp_series = series.dropna().dt
        time_val_map = {"hour": 0, "minute": 0, "second": 0}
        return all(
            getattr(temp_series, time_part).eq(val).all()
            for time_part, val in time_val_map.items()
        )

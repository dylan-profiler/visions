from typing import Sequence

import pandas as pd
from pandas.api import types as pdt

from visions.relations import IdentityRelation, TypeRelation
from visions.types.type import VisionsBaseType
from visions.utils.series_utils import series_not_empty, series_not_sparse


def _get_relations(cls) -> Sequence[TypeRelation]:
    from visions.types import Integer

    relations = [IdentityRelation(cls, Integer)]
    return relations


class Count(VisionsBaseType):
    """**Count** (positive integer) implementation of :class:`visions.types.type.VisionsBaseType`.

    Examples:
        >>> x = pd.Series([1, 4, 10, 20])
        >>> x in visions.Count
        True
    """

    @classmethod
    def get_relations(cls) -> Sequence[TypeRelation]:
        return _get_relations(cls)

    @classmethod
    @series_not_sparse
    @series_not_empty
    def contains_op(cls, series: pd.Series, state: dict) -> bool:
        return pdt.is_unsigned_integer_dtype(series)

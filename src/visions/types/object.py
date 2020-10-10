from typing import Sequence

import pandas as pd
from pandas.api import types as pdt

from visions.relations import IdentityRelation, TypeRelation
from visions.types.type import VisionsBaseType
from visions.utils.series_utils import (
    nullable_series_contains,
    series_not_empty,
    series_not_sparse,
)


def _get_relations(cls) -> Sequence[TypeRelation]:
    from visions.types import Generic

    relations = [IdentityRelation(cls, Generic)]
    return relations


pandas_has_string_dtype_flag = hasattr(pdt, "is_string_dtype")


class Object(VisionsBaseType):
    """**Object** implementation of :class:`visions.types.type.VisionsBaseType`.

    Examples:
        >>> x = pd.Series(['a', 1, np.nan])
        >>> x in visions.Object
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
        is_object = pdt.is_object_dtype(series)
        if is_object:
            ret = True
        elif pandas_has_string_dtype_flag:
            ret = pdt.is_string_dtype(series) and not pdt.is_categorical_dtype(series)
        else:
            ret = False
        return ret

from typing import Sequence

import pandas as pd
from pandas.api import types as pdt

from visions.relations import IdentityRelation, TypeRelation
from visions.types.type import VisionsBaseType
from visions.utils import func_nullable_series_contains
from visions.utils.series_utils import series_not_empty, series_not_sparse


@func_nullable_series_contains
def series_is_string(series: pd.Series, state: dict):
    return all(isinstance(v, str) for v in series)


def _get_relations(cls) -> Sequence[TypeRelation]:
    from visions.types import Object

    relations = [IdentityRelation(cls, Object)]
    return relations


pandas_has_string_dtype_flag = hasattr(pdt, "is_string_dtype")


class String(VisionsBaseType):
    """**String** implementation of :class:`visions.types.type.VisionsBaseType`.

    Examples:
        >>> x = pd.Series(['rubin', 'carter', 'champion'])
        >>> x in visions.String
        True
    """

    @classmethod
    def get_relations(cls) -> Sequence[TypeRelation]:
        return _get_relations(cls)

    @classmethod
    @series_not_sparse
    @series_not_empty
    def contains_op(cls, series: pd.Series, state: dict) -> bool:
        # TODO: without the object check this passes string categories... is there a better way?
        if pdt.is_categorical_dtype(series):
            return False
        elif not pdt.is_object_dtype(series):
            return pandas_has_string_dtype_flag and pdt.is_string_dtype(series)

        return series_is_string(series)

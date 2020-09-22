from typing import List, Sequence

import numpy as np
import pandas as pd
from pandas.api import types as pdt

from visions.relations import IdentityRelation, InferenceRelation, TypeRelation
from visions.types.type import VisionsBaseType
from visions.utils import func_nullable_series_contains
from visions.utils.series_utils import series_not_empty, series_not_sparse


def to_int(series: pd.Series, state: dict) -> pd.Series:
    dtype = "Int64" if series.hasnans else np.int64
    return series.astype(dtype)


@func_nullable_series_contains
def float_is_int(series: pd.Series, state: dict) -> bool:
    def check_equality(series):
        try:
            if not np.isfinite(series).all():
                return False
            return series.eq(series.astype(int)).all()
        except:
            return False

    return check_equality(series)


def _get_relations(cls) -> List[TypeRelation]:
    from visions.types import Float, Generic

    relations = [
        IdentityRelation(cls, Generic),
        InferenceRelation(cls, Float, relationship=float_is_int, transformer=to_int),
    ]
    return relations


class Integer(VisionsBaseType):
    """**Integer** implementation of :class:`visions.types.type.VisionsBaseType`.

    Examples:
        >>> x = pd.Series([1, 2, 3])
        >>> x in visions.Integer
        True
    """

    @classmethod
    def get_relations(cls) -> Sequence[TypeRelation]:
        return _get_relations(cls)

    @classmethod
    @series_not_sparse
    @series_not_empty
    def contains_op(cls, series: pd.Series, state: dict) -> bool:
        return pdt.is_integer_dtype(series)

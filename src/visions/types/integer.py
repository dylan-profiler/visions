from typing import Sequence, List

import pandas.api.types as pdt
import pandas as pd
import numpy as np

from visions.relations import IdentityRelation, InferenceRelation, TypeRelation
from visions.types import VisionsBaseType
from visions.utils.coercion import test_utils


def to_int(series: pd.Series) -> pd.Series:
    try:
        return series.astype(int)
    except ValueError:
        return series.astype("Int64")


def float_is_int(series: pd.Series) -> bool:
    def check_equality(series):
        if series.empty or not np.isfinite(series).all():
            return False
        return series.eq(series.astype(int)).all()

    return check_equality(series.dropna() if series.hasnans else series)


def _get_relations(cls) -> List[TypeRelation]:
    from visions.types import String, Generic, Float

    relations = [
        IdentityRelation(cls, Generic),
        InferenceRelation(cls, Float, relationship=float_is_int, transformer=to_int),
        InferenceRelation(
            cls,
            String,
            relationship=test_utils.coercion_test(to_int),
            transformer=to_int,
        ),
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
    def contains_op(cls, series: pd.Series) -> bool:
        return pdt.is_signed_integer_dtype(series)

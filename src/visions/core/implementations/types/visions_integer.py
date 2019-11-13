import pandas.api.types as pdt
import pandas as pd
import numpy as np

from visions.core.model.relations import IdentityRelation, InferenceRelation
from visions.core.model.type import VisionsBaseType
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


def _get_relations():
    from visions.core.implementations.types import (
        visions_string,
        visions_generic,
        visions_float,
    )

    relations = [
        IdentityRelation(visions_integer, visions_generic),
        InferenceRelation(
            visions_integer,
            visions_float,
            relationship=float_is_int,
            transformer=to_int,
        ),
        InferenceRelation(
            visions_integer,
            visions_string,
            relationship=test_utils.coercion_test(to_int),
            transformer=to_int,
        ),
    ]
    return relations


class visions_integer(VisionsBaseType):
    """**Integer** implementation of :class:`visions.core.model.type.VisionsBaseType`.

    Examples:
        >>> x = pd.Series([1, 2, 3])
        >>> x in visions_integer
        True
    """

    @classmethod
    def get_relations(cls):
        return _get_relations()

    @classmethod
    def contains_op(cls, series: pd.Series) -> bool:
        return pdt.is_signed_integer_dtype(series)

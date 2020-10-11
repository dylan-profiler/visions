from functools import partial
from typing import Sequence

import pandas as pd
from pandas.api import types as pdt

from visions.relations import IdentityRelation, InferenceRelation, TypeRelation
from visions.relations.string_to_bool import get_boolean_coercions
from visions.types.type import VisionsBaseType
from visions.utils import func_nullable_series_contains
from visions.utils.coercion.test_utils import coercion_map, coercion_map_test
from visions.utils.series_utils import series_not_empty, series_not_sparse

hasnan_bool_name = "boolean" if int(pd.__version__.split(".")[0]) >= 1 else "Bool"


def to_bool(series: pd.Series, state: dict) -> pd.Series:
    dtype = hasnan_bool_name if series.hasnans else bool
    return series.astype(dtype)


@func_nullable_series_contains
def object_is_bool(series: pd.Series, state: dict) -> bool:
    bool_set = {True, False}
    try:
        ret = all(item in bool_set for item in series)
    except:
        ret = False

    return ret


def string_is_bool(series, state: dict, string_coercions):
    try:
        return coercion_map_test(string_coercions)(series.str.lower())
    except:
        return False


def string_to_bool(series, state: dict, string_coercions):
    try:
        return to_bool(coercion_map(string_coercions)(series.str.lower()), state)
    except:
        return False


def _get_relations(cls) -> Sequence[TypeRelation]:
    from visions.types import Generic, Object, String

    relations = [
        IdentityRelation(cls, Generic),
        InferenceRelation(
            cls,
            String,
            relationship=partial(string_is_bool, string_coercions=cls.string_coercions),
            transformer=partial(string_to_bool, string_coercions=cls.string_coercions),
        ),
        InferenceRelation(
            cls, Object, relationship=object_is_bool, transformer=to_bool
        ),
    ]
    return relations


class Boolean(VisionsBaseType):
    """**Boolean** implementation of :class:`visions.types.type.VisionsBaseType`.

    Examples:
        >>> x = pd.Series([True, False, False, True])
        >>> x in visions.Boolean
        True

        >>> x = pd.Series([True, False, None])
        >>> x in visions.Boolean
        True
    """

    string_coercions = get_boolean_coercions("en")

    @classmethod
    def get_relations(cls) -> Sequence[TypeRelation]:
        return _get_relations(cls)

    @classmethod
    @series_not_sparse
    @series_not_empty
    def contains_op(cls, series: pd.Series, state: dict) -> bool:
        if not pdt.is_categorical_dtype(series) and pdt.is_bool_dtype(series):
            return True

        return False

    @classmethod
    def make_string_coercion(cls, type_name, string_coercions):
        @classmethod
        def get_relations(cls):
            return _get_relations(cls)

        name = cls.__name__
        return type(
            f"{name}[{type_name}]",
            (cls,),
            {
                "string_coercions": string_coercions,
                "get_relations": get_relations,
                "contains_op": cls.contains_op,
                "make_string_coercion": cls.make_string_coercion,
            },
        )

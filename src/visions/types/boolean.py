from functools import partial
from typing import Sequence

import pandas as pd
from pandas.api import types as pdt

from visions.relations import IdentityRelation, InferenceRelation, TypeRelation
from visions.relations.string_to_bool import get_boolean_coercions
from visions.types.type import VisionsBaseType
from visions.utils.coercion.test_utils import coercion_map, coercion_map_test

hasnan_bool_name = "boolean" if int(pd.__version__.split(".")[0]) >= 1 else "Bool"


def to_bool(series: pd.Series, state: dict) -> pd.Series:
    hasnans = state.get("hasnans")
    dtype = hasnan_bool_name if hasnans else bool
    return series.astype(dtype)


def object_is_bool(series: pd.Series, state: dict) -> bool:
    # TODO: use coercion in helpers?
    bool_set = {True, False}
    try:
        ret = all(item in bool_set for item in series)
    except:
        ret = False

    return ret


def string_is_bool(series, state: dict, string_coercions):
    return coercion_map_test(string_coercions)(series.str.lower())


def string_to_bool(series, state: dict, string_coercions):
    return to_bool(coercion_map(string_coercions)(series.str.lower()), state)


def _get_relations(cls) -> Sequence[TypeRelation]:
    from visions.types import Object, Optional, String

    relations = [
        IdentityRelation(cls, Optional),
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
    def contains_op(cls, series: pd.Series, state: dict) -> bool:
        if not pdt.is_categorical_dtype(series) and pdt.is_bool_dtype(series):
            return True

        return False

    @classmethod
    def make_string_coercion(cls, type_name, string_coercions):
        @classmethod
        def get_relations(cls):
            return _get_relations(cls)

        return type(
            "{name}[{type_name}]".format(name=cls.__name__, type_name=type_name),
            (cls,),
            {
                "string_coercions": string_coercions,
                "get_relations": get_relations,
                "contains_op": cls.contains_op,
                "make_string_coercion": cls.make_string_coercion,
            },
        )

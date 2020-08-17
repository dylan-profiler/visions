from typing import Sequence

import numpy as np
import pandas as pd
from pandas.api import types as pdt

from visions.relations import IdentityRelation, InferenceRelation, TypeRelation
from visions.relations.string_to_bool import get_boolean_coercions
from visions.types.type import VisionsBaseType
from visions.utils.coercion.test_utils import coercion_map, coercion_map_test


def to_bool(series: pd.Series) -> pd.Series:
    return series.astype("Bool" if series.hasnans else bool)


def object_is_bool(series: pd.Series) -> bool:
    bool_set = {True, False, None, np.nan}
    try:
        ret = all(item in bool_set for item in series)
    except:
        ret = False

    return ret


def _get_relations(cls) -> Sequence[TypeRelation]:
    from visions.types import Generic, Object, String

    relations = [
        IdentityRelation(cls, Generic),
        InferenceRelation(
            cls,
            String,
            relationship=lambda s: coercion_map_test(cls.string_coercions)(
                s.str.lower()
            ),
            transformer=lambda s: to_bool(
                coercion_map(cls.string_coercions)(s.str.lower())
            ),
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
    def contains_op(cls, series: pd.Series) -> bool:
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

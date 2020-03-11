from typing import Sequence

import numpy as np
import pandas as pd
import pandas.api.types as pdt

from visions.relations import IdentityRelation, InferenceRelation, TypeRelation
from visions.relations.string_to_bool import get_boolean_coercions
from visions.types import VisionsBaseType
from visions.utils.coercion.test_utils import coercion_map_test, coercion_map


def to_bool(series: pd.Series) -> pd.Series:
    if series.isin({True, False}).all():
        return series.astype(bool)
    elif series.isin({True, False, None, np.nan}).all():
        return series.astype("Bool")
    else:
        unsupported_values = series[~series.isin({True, False, None, np.nan})].unique()
        raise ValueError(
            "Values not supported {unsupported_values}".format(
                unsupported_values=unsupported_values
            )
        )


def _get_relations(cls) -> Sequence[TypeRelation]:
    from visions.types import Generic, String, Integer, Object

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
            cls,
            Integer,
            relationship=lambda s: s.isin({0, 1, np.nan}).all(),
            transformer=to_bool,
        ),
        InferenceRelation(
            cls,
            Object,
            relationship=lambda s: s.apply(type).isin([type(None), bool]).all(),
            transformer=to_bool,
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
        return not pdt.is_categorical_dtype(series) and pdt.is_bool_dtype(series)

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

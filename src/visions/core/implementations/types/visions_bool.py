import numpy as np
import pandas as pd
import pandas.api.types as pdt

from visions.core.model.relations import IdentityRelation, InferenceRelation
from visions.core.model.type import VisionsBaseType
from visions.lib.relations.string_to_bool import get_boolean_coercions
from visions.utils.coercion.test_utils import coercion_map_test, coercion_map


def to_bool(series: pd.Series) -> pd.Series:
    if series.isin({True, False}).all():
        return series.astype(bool)
    elif series.isin({True, False, None, np.nan}).all():
        return series.astype("Bool")
    else:
        unsupported_values = series[~series.isin({True, False, None, np.nan})].unique()
        raise ValueError(f"Values not supported {unsupported_values}")


def _get_relations(cls) -> dict:
    from visions.core.implementations.types import (
        visions_generic,
        visions_string,
        visions_integer,
        visions_object,
    )

    relations = [
        IdentityRelation(visions_bool, visions_generic),
        InferenceRelation(
            visions_bool,
            visions_string,
            relationship=lambda s: coercion_map_test(cls.string_coercions)(
                s.str.lower()
            ),
            transformer=lambda s: to_bool(
                coercion_map(cls.string_coercions)(s.str.lower())
            ),
        ),
        InferenceRelation(
            visions_bool,
            visions_integer,
            relationship=lambda s: s.isin({0, 1, np.nan}).all(),
            transformer=to_bool,
        ),
        InferenceRelation(
            visions_bool,
            visions_object,
            relationship=lambda s: s.apply(type).isin([type(None), bool]).all(),
            transformer=to_bool,
        ),
    ]
    return relations


class visions_bool(VisionsBaseType):
    """**Boolean** implementation of :class:`visions.core.model.type.VisionsBaseType`.

    Examples:
        >>> x = pd.Series([True, False, False, True])
        >>> x in visions_bool
        True

        >>> x = pd.Series([True, False, None])
        >>> x in visions_bool
        True
    """

    string_coercions = get_boolean_coercions("en")

    @classmethod
    def get_relations(cls) -> dict:
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
            f"{cls.__name__}[{type_name}]",
            (cls,),
            {
                "string_coercions": string_coercions,
                "get_relations": get_relations,
                "contains_op": cls.contains_op,
                "make_string_coercion": cls.make_string_coercion,
            },
        )

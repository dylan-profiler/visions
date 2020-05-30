from typing import List, Sequence

import numpy as np
import pandas as pd
from pandas.api import types as pdt

from visions.relations import IdentityRelation, InferenceRelation, TypeRelation
from visions.types import Integer, Object, String, VisionsBaseType
from visions.utils.coercion.test_utils import coercion_map, coercion_map_test


def to_category(series: pd.Series) -> pd.Series:
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


def _get_relations(cls) -> List[TypeRelation]:
    from visions.types import Generic

    relations = [
        IdentityRelation(cls, Generic),
        InferenceRelation(
            cls,
            String,
            relationship=lambda s: coercion_map_test(cls.string_coercions)(
                s.str.lower()
            ),
            transformer=lambda s: to_category(
                coercion_map(cls.string_coercions)(s.str.lower())
            ),
        ),
        InferenceRelation(
            cls,
            Integer,
            relationship=lambda s: s.isin({0, 1, np.nan}).all(),
            transformer=to_category,
        ),
        InferenceRelation(
            cls,
            Object,
            relationship=lambda s: s.apply(type).isin([type(None), bool]).all(),
            transformer=to_category,
        ),
    ]
    return relations


class Category(VisionsBaseType):
    """**Categorical** implementation of :class:`visions.types.type.VisionsBaseType`.

    Examples:
        >>> x = pd.Series([True, False, 1], dtype='category')
        >>> x in visions.Category
        True
    """

    @classmethod
    def get_relations(cls) -> Sequence[TypeRelation]:
        return _get_relations(cls)

    @classmethod
    def contains_op(cls, series: pd.Series) -> bool:
        return pdt.is_categorical_dtype(series) or pdt.is_bool_dtype(series)

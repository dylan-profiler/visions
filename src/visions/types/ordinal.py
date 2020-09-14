from typing import Sequence

import pandas as pd
from pandas.api import types as pdt

from visions.relations import IdentityRelation, TypeRelation
from visions.types.type import VisionsBaseType
from visions.utils.series_utils import series_not_empty


def to_ordinal(series: pd.Series) -> pd.Categorical:
    return pd.Categorical(
        series, categories=sorted(series.dropna().unique()), ordered=True
    )


def _get_relations(cls) -> Sequence[TypeRelation]:
    from visions.types import Categorical

    relations = [IdentityRelation(cls, Categorical)]
    return relations


class Ordinal(VisionsBaseType):
    """**Ordinal** implementation of :class:`visions.types.type.VisionsBaseType`.

    Examples:
        >>> x = pd.Series([1, 2, 3, 1, 1], dtype='category')
        >>> x in visions.Ordinal
        True
    """

    @classmethod
    def get_relations(cls) -> Sequence[TypeRelation]:
        return _get_relations(cls)

    @classmethod
    @series_not_empty
    def contains_op(cls, series: pd.Series, state: dict) -> bool:
        return pdt.is_categorical_dtype(series) and series.cat.ordered

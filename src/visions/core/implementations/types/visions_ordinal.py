from typing import Sequence

import pandas.api.types as pdt
import pandas as pd

from visions.core.model.relations import IdentityRelation
from visions.core.model import TypeRelation
from visions.core.model.type import VisionsBaseType


def to_ordinal(series: pd.Series) -> pd.Categorical:
    return pd.Categorical(
        series, categories=sorted(series.dropna().unique()), ordered=True
    )


def _get_relations(cls) -> Sequence[TypeRelation]:
    from visions.core.implementations.types import visions_categorical

    relations = [IdentityRelation(cls, visions_categorical)]
    return relations


class visions_ordinal(VisionsBaseType):
    """**Ordinal** implementation of :class:`visions.core.model.type.VisionsBaseType`.

    Examples:
        >>> x = pd.Series([1, 2, 3, 1, 1], dtype='category')
        >>> x in visions_ordinal
        True
    """

    @classmethod
    def get_relations(cls) -> Sequence[TypeRelation]:
        return _get_relations(cls)

    @classmethod
    def contains_op(cls, series: pd.Series) -> bool:
        return pdt.is_categorical_dtype(series) and series.cat.ordered

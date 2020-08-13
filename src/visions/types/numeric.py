from typing import List, Sequence

import numpy as np
import pandas as pd
import pandas.api.types as pdt

from visions.types import Generic
from visions.relations import IdentityRelation, InferenceRelation, TypeRelation
from visions.types.type import VisionsBaseType
from visions.utils.coercion import test_utils


def _get_relations(cls) -> Sequence[TypeRelation]:
    relations = [IdentityRelation(cls, Generic)]
    return relations


class Numeric(VisionsBaseType):
    """**Numeric** implementation of :class:`visions.types.type.VisionsBaseType`.

    Examples:
        >>> x = pd.Series([1, 2, 3])
        >>> x in visions.Numeric
        True
    """

    @classmethod
    def get_relations(cls) -> Sequence[TypeRelation]:
        return _get_relations(cls)

    @classmethod
    def contains_op(cls, series: pd.Series) -> bool:
        return pdt.is_numeric(series)

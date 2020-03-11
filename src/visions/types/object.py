from typing import Sequence

import pandas.api.types as pdt
import pandas as pd

from visions.relations import IdentityRelation, TypeRelation
from visions.types import VisionsBaseType


def _get_relations(cls) -> Sequence[TypeRelation]:
    from visions.types import Generic

    relations = [IdentityRelation(cls, Generic)]
    return relations


class Object(VisionsBaseType):
    """**Object** implementation of :class:`visions.types.type.VisionsBaseType`.

    Examples:
        >>> x = pd.Series(['a', 1, np.nan])
        >>> x in visions.Object
        True
    """

    @classmethod
    def get_relations(cls) -> Sequence[TypeRelation]:
        return _get_relations(cls)

    @classmethod
    def contains_op(cls, series: pd.Series) -> bool:
        return pdt.is_object_dtype(series)

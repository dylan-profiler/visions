import pandas.api.types as pdt
import pandas as pd
from typing import Sequence

from visions.core.model.relations import (
    IdentityRelation,
    InferenceRelation,
    TypeRelation,
)
from visions.core.model.type import VisionsBaseType


def _get_relations() -> Sequence[TypeRelation]:
    from visions.core.implementations.types import visions_generic

    relations = [IdentityRelation(visions_object, visions_generic)]
    return relations


class visions_object(VisionsBaseType):
    """**Object** implementation of :class:`visions.core.model.type.VisionsBaseType`.

    Examples:
        >>> x = pd.Series(['a', 1, np.nan])
        >>> x in visions_object
        True
    """

    @classmethod
    def get_relations(cls) -> Sequence[TypeRelation]:
        return _get_relations()

    @classmethod
    def contains_op(cls, series: pd.Series) -> bool:
        return pdt.is_object_dtype(series)

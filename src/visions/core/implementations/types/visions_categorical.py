import pandas.api.types as pdt
import pandas as pd

from visions.core.model.relations import IdentityRelation
from visions.core.model.type import VisionsBaseType


def _get_relations():
    from visions.core.implementations.types import visions_generic

    relations = [IdentityRelation(visions_categorical, visions_generic)]
    return relations


class visions_categorical(VisionsBaseType):
    """**Categorical** implementation of :class:`visions.core.model.type.VisionsBaseType`.

    Examples:
        >>> x = pd.Series([True, False, 1], dtype='category')
        >>> x in visions_categorical
        True
    """

    @classmethod
    def get_relations(cls) -> dict:
        return _get_relations()

    @classmethod
    def contains_op(cls, series: pd.Series) -> bool:
        return pdt.is_categorical_dtype(series)

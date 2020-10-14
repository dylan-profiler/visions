from typing import Any, Sequence

from multimethod import multimethod

from visions.relations import IdentityRelation, TypeRelation
from visions.types.categorical import Categorical
from visions.types.type import VisionsBaseType


class Ordinal(VisionsBaseType):
    """**Ordinal** implementation of :class:`visions.types.type.VisionsBaseType`.

    Examples:
        >>> import pandas as pd
        >>> import visions
        >>> x = pd.Series([1, 2, 3, 1, 1], dtype='category')
        >>> x in visions.Ordinal
        True
    """

    @classmethod
    def get_relations(cls) -> Sequence[TypeRelation]:
        relations = [IdentityRelation(cls, Categorical)]
        return relations

    @staticmethod
    @multimethod
    def contains_op(item: Any, state: dict) -> bool:
        pass

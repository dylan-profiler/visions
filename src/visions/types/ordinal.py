from functools import singledispatch
from typing import Iterable, Sequence

from visions.relations import IdentityRelation, TypeRelation
from visions.types.type import VisionsBaseType


@singledispatch
def ordinal_contains(sequence: Iterable, state: dict) -> bool:
    return False


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
        from visions.types import Categorical

        relations = [IdentityRelation(cls, Categorical)]
        return relations

    @classmethod
    def contains_op(cls, sequence: Iterable, state: dict) -> bool:
        return ordinal_contains(sequence, state)

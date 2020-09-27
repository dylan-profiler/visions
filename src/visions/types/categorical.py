from functools import singledispatch
from typing import Iterable, Sequence

from visions.relations import IdentityRelation, TypeRelation
from visions.types.type import VisionsBaseType


@singledispatch
def categorical_contains(sequence: Iterable, state: dict) -> bool:
    return False


class Categorical(VisionsBaseType):
    """**Categorical** implementation of :class:`visions.types.type.VisionsBaseType`.

    Examples:
        >>> import pandas as pd
        >>> import visions
        >>> x = pd.Series([True, False, 1], dtype='category')
        >>> x in visions.Categorical
        True
    """

    @classmethod
    def get_relations(cls) -> Sequence[TypeRelation]:
        from visions.types import Generic

        relations = [IdentityRelation(cls, Generic)]
        return relations

    @classmethod
    def contains_op(cls, sequence: Iterable, state: dict) -> bool:
        return categorical_contains(sequence, state)

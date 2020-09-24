from functools import singledispatch
from typing import Iterable, Sequence

from visions.relations import IdentityRelation, TypeRelation
from visions.types.type import VisionsBaseType


@singledispatch
def count_contains(sequence: Iterable, state: dict) -> bool:
    return all(isinstance(value, int) and value >= 0 for value in sequence)


class Count(VisionsBaseType):
    """**Count** (positive integer) implementation of :class:`visions.types.type.VisionsBaseType`.

    Examples:
        >>> x = [1, 4, 10, 20]
        >>> x in visions.Count
        True
    """

    @classmethod
    def get_relations(cls) -> Sequence[TypeRelation]:
        from visions.types import Integer

        relations = [IdentityRelation(cls, Integer)]
        return relations

    @classmethod
    def contains_op(cls, sequence: Iterable, state: dict) -> bool:
        return count_contains(sequence, state)

from functools import singledispatch
from typing import Iterable, Sequence

from visions.relations import IdentityRelation, TypeRelation
from visions.types.type import VisionsBaseType


@singledispatch
def string_contains(sequence: Iterable, state: dict) -> bool:
    return all(isinstance(v, str) for v in sequence)


class String(VisionsBaseType):
    """**String** implementation of :class:`visions.types.type.VisionsBaseType`.

    Examples:
        >>> x = ['rubin', 'carter', 'champion']
        >>> x in visions.String
        True
    """

    @classmethod
    def get_relations(cls) -> Sequence[TypeRelation]:
        from visions.types import Object

        relations = [IdentityRelation(cls, Object)]
        return relations

    @classmethod
    def contains_op(cls, sequence: Iterable, state: dict) -> bool:
        return string_contains(sequence, state)

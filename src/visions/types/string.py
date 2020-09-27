from functools import singledispatch
from typing import Iterable, Sequence

from visions.backends.python.series_utils import (
    sequence_handle_none,
    sequence_not_empty,
)
from visions.relations import IdentityRelation, TypeRelation
from visions.types.type import VisionsBaseType


@singledispatch
@sequence_not_empty
@sequence_handle_none
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

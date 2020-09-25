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
def object_contains(sequence: Iterable, state: dict) -> bool:
    return any(not isinstance(value, (float, bool, int, complex)) for value in sequence)


class Object(VisionsBaseType):
    """**Object** implementation of :class:`visions.types.type.VisionsBaseType`.

    Examples:
        >>> x = ['a', 1, np.nan]
        >>> x in visions.Object
        True
    """

    @classmethod
    def get_relations(cls) -> Sequence[TypeRelation]:
        from visions.types import Generic

        relations = [IdentityRelation(cls, Generic)]
        return relations

    @classmethod
    def contains_op(cls, sequence: Iterable, state: dict) -> bool:
        return object_contains(sequence, state)

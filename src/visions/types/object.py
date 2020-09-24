from functools import singledispatch
from typing import Iterable, Sequence

from visions.relations import IdentityRelation, TypeRelation
from visions.types.type import VisionsBaseType


@singledispatch
def object_contains(sequence: Iterable, state: dict) -> bool:
    return True


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

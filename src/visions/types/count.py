from typing import Any, Sequence

from multimethod import multimethod

from visions.relations import IdentityRelation, TypeRelation
from visions.types.integer import Integer
from visions.types.type import VisionsBaseType


class Count(VisionsBaseType):
    """**Count** (positive integer) implementation of :class:`visions.types.type.VisionsBaseType`.

    Examples:
        >>> x = [1, 4, 10, 20]
        >>> x in visions.Count
        True
    """

    @classmethod
    def get_relations(cls) -> Sequence[TypeRelation]:
        relations = [IdentityRelation(cls, Integer)]
        return relations

    @staticmethod
    @multimethod
    def contains_op(item: Any, state: dict) -> bool:
        pass

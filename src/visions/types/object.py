from typing import Any, Sequence

from multimethod import multimethod

from visions.relations import IdentityRelation, TypeRelation
from visions.types.generic import Generic
from visions.types.type import VisionsBaseType


class Object(VisionsBaseType):
    """**Object** implementation of :class:`visions.types.type.VisionsBaseType`.

    Examples:
        >>> x = ['a', 1, np.nan]
        >>> x in visions.Object
        True
    """

    @classmethod
    def get_relations(cls) -> Sequence[TypeRelation]:
        relations = [IdentityRelation(cls, Generic)]
        return relations

    @staticmethod
    @multimethod
    def contains_op(item: Any, state: dict) -> bool:
        pass

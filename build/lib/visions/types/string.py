from typing import Any, Sequence

from multimethod import multimethod

from visions.relations import IdentityRelation, TypeRelation
from visions.types.object import Object
from visions.types.type import VisionsBaseType


class String(VisionsBaseType):
    """**String** implementation of :class:`visions.types.type.VisionsBaseType`.

    Examples:
        >>> x = ['rubin', 'carter', 'champion']
        >>> x in visions.String
        True
    """

    @staticmethod
    def get_relations() -> Sequence[TypeRelation]:
        relations = [IdentityRelation(Object)]
        return relations

    @staticmethod
    @multimethod
    def contains_op(item: Any, state: dict) -> bool:
        pass

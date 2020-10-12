from typing import Any, Sequence

from multimethod import multimethod

from visions.relations import IdentityRelation, TypeRelation
from visions.types.object import Object
from visions.types.type import VisionsBaseType


class Time(VisionsBaseType):
    """**Time** implementation of :class:`visions.types.type.VisionsBaseType`.

    Examples:
        >>> import datetime
        >>> import visions
        >>> x = [datetime.time(10, 8, 4), datetime.time(21, 17, 0)]
        >>> x in visions.Time
        True
    """

    @classmethod
    def get_relations(cls) -> Sequence[TypeRelation]:
        relations = [IdentityRelation(cls, Object)]
        return relations

    @staticmethod
    @multimethod
    def contains_op(item: Any, state: dict) -> bool:
        pass

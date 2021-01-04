from typing import Any, Sequence

from multimethod import multimethod

from visions.relations import IdentityRelation, TypeRelation
from visions.types.generic import Generic
from visions.types.type import VisionsBaseType


class TimeDelta(VisionsBaseType):
    """**TimeDelta** implementation of :class:`visions.types.type.VisionsBaseType`.

    Examples:
        >>> from datetime import timedelta
        >>> x = [timedelta(hours=1), timedelta(hours=3)]
        >>> x in visions.Timedelta
        True
    """

    @staticmethod
    def get_relations() -> Sequence[TypeRelation]:
        relations = [IdentityRelation(Generic)]
        return relations

    @staticmethod
    @multimethod
    def contains_op(item: Any, state: dict) -> bool:
        pass

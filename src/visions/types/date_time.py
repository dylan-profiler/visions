from typing import Any, Sequence

from multimethod import multimethod

from visions.relations import IdentityRelation, InferenceRelation, TypeRelation
from visions.types.generic import Generic
from visions.types.string import String
from visions.types.type import VisionsBaseType


class DateTime(VisionsBaseType):
    """**Datetime** implementation of :class:`visions.types.type.VisionsBaseType`.

    Examples:
        >>> import datetime
        >>> import visions
        >>> x = [datetime.datetime(2017, 3, 5), datetime.datetime(2019, 12, 4)]
        >>> x in visions.DateTime
        True
    """

    @staticmethod
    def get_relations() -> Sequence[TypeRelation]:
        relations = [
            IdentityRelation(Generic),
            InferenceRelation(String),
        ]
        return relations

    @staticmethod
    @multimethod
    def contains_op(item: Any, state: dict) -> bool:
        pass

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

    @classmethod
    def get_relations(cls) -> Sequence[TypeRelation]:
        relations = [
            IdentityRelation(cls, Generic),
            InferenceRelation(
                cls,
                String,
            ),
        ]
        return relations

    @staticmethod
    @multimethod
    def contains_op(item: Any, state: dict) -> bool:
        pass

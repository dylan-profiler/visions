from typing import Any, Sequence

from multimethod import multimethod

from visions.relations import IdentityRelation, InferenceRelation, TypeRelation
from visions.types.date_time import DateTime
from visions.types.object import Object
from visions.types.type import VisionsBaseType


class Date(VisionsBaseType):
    """**Date** implementation of :class:`visions.types.type.VisionsBaseType`.
    All values are should be datetime.date or missing

    Examples:
        >>> import datetime
        >>> import visions
        >>> x = [datetime.date(2017, 3, 5), datetime.date(2019, 12, 4)]
        >>> x in visions.Date
        True
    """

    @staticmethod
    def get_relations() -> Sequence[TypeRelation]:
        relations = [
            IdentityRelation(Object),
            InferenceRelation(DateTime),
        ]
        return relations

    @staticmethod
    @multimethod
    def contains_op(item: Any, state: dict) -> bool:
        pass

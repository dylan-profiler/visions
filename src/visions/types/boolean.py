from typing import Any, Sequence

from multimethod import multimethod

from visions.relations import IdentityRelation, InferenceRelation, TypeRelation
from visions.types.generic import Generic
from visions.types.object import Object
from visions.types.string import String
from visions.types.type import VisionsBaseType


class Boolean(VisionsBaseType):
    """**Boolean** implementation of :class:`visions.types.type.VisionsBaseType`.

    Examples:
        >>> import visions
        >>> x = [True, False, False, True]
        >>> x in visions.Boolean
        True

        >>> x = [True, False, None]
        >>> x in visions.Boolean
        True
    """

    @classmethod
    def get_relations(cls) -> Sequence[TypeRelation]:
        relations = [
            IdentityRelation(cls, Generic),
            InferenceRelation(cls, String),
            InferenceRelation(cls, Object),
        ]
        return relations

    @staticmethod
    @multimethod
    def contains_op(item: Any, state: dict) -> bool:
        print("?")
        pass

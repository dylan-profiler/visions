from typing import Any, Sequence

from multimethod import multimethod

from visions.relations import IdentityRelation, InferenceRelation, TypeRelation
from visions.types.complex import Complex
from visions.types.generic import Generic
from visions.types.string import String
from visions.types.type import VisionsBaseType


class Float(VisionsBaseType):
    """**Float** implementation of :class:`visions.types.type.VisionsBaseType`.

    Examples:
        >>> import visions
        >>> x = [1.0, 2.5, 5.0]
        >>> x in visions.Float
        True
    """

    @staticmethod
    def get_relations() -> Sequence[TypeRelation]:
        relations = [
            IdentityRelation(Generic),
            InferenceRelation(String),
            InferenceRelation(Complex),
        ]
        return relations

    @staticmethod
    @multimethod
    def contains_op(item: Any, state: dict) -> bool:
        pass

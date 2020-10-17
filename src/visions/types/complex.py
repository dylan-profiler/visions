from typing import Any, Sequence

from multimethod import multimethod

from visions.relations import IdentityRelation, InferenceRelation, TypeRelation
from visions.types.generic import Generic
from visions.types.string import String
from visions.types.type import VisionsBaseType


class Complex(VisionsBaseType):
    """**Complex** implementation of :class:`visions.types.type.VisionsBaseType`.

    Examples:
        >>> x = [complex(0, 0), complex(1, 2), complex(3, -1)]
        >>> x in visions.Complex
        True
    """

    @classmethod
    def get_relations(cls) -> Sequence[TypeRelation]:
        relations = [
            IdentityRelation(cls, Generic),
            InferenceRelation(cls, String),
        ]
        return relations

    @staticmethod
    @multimethod
    def contains_op(item: Any, state: dict) -> bool:
        pass

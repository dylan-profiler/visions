from typing import Any, Sequence

from multimethod import multimethod

from visions.relations import IdentityRelation, InferenceRelation, TypeRelation
from visions.types.float import Float
from visions.types.generic import Generic
from visions.types.type import VisionsBaseType


class Integer(VisionsBaseType):
    """**Integer** implementation of :class:`visions.types.type.VisionsBaseType`.
    Examples:
        >>> import pandas as pd
        >>> x = [-1, 1, 2, 3]
        >>> x in visions.Integer
        True
    """

    @classmethod
    def get_relations(cls) -> Sequence[TypeRelation]:
        relations = [
            IdentityRelation(cls, Generic),
            InferenceRelation(
                cls,
                Float,
            ),
        ]
        return relations

    @staticmethod
    @multimethod
    def contains_op(item: Any, state: dict) -> bool:
        pass

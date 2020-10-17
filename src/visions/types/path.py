from typing import Any, Sequence

from multimethod import multimethod

from visions.relations import IdentityRelation, InferenceRelation, TypeRelation
from visions.types.object import Object
from visions.types.string import String
from visions.types.type import VisionsBaseType


class Path(VisionsBaseType):
    """**Path** implementation of :class:`visions.types.type.VisionsBaseType`.

    Examples:
        >>> import pathlib
        >>> import visions
        >>> x = [pathlib.Path('/home/user/file.txt'), pathlib.Path('/home/user/test2.txt')]
        >>> x in visions.Path
        True
    """

    @classmethod
    def get_relations(cls) -> Sequence[TypeRelation]:
        relations = [
            IdentityRelation(cls, Object),
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

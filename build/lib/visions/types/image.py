from typing import Any, Sequence

from multimethod import multimethod

from visions.relations import IdentityRelation, TypeRelation
from visions.types.file import File
from visions.types.type import VisionsBaseType


class Image(VisionsBaseType):
    """**Image** implementation of :class:`visions.types.type.VisionsBaseType`.
    (i.e. series with all image files)

    Examples:
        >>> from pathlib import Path
        >>> import visions
        >>> x = [Path('/home/user/file.png'), Path('/home/user/test2.jpg')]
        >>> x in visions.Image
        True
    """

    @staticmethod
    def get_relations() -> Sequence[TypeRelation]:
        relations = [IdentityRelation(File)]
        return relations

    @staticmethod
    @multimethod
    def contains_op(item: Any, state: dict) -> bool:
        pass

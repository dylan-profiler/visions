import imghdr
from functools import singledispatch
from pathlib import Path
from typing import Iterable, Sequence

from visions.relations import IdentityRelation, TypeRelation
from visions.types.type import VisionsBaseType


@singledispatch
def image_contains(sequence: Iterable, state: dict) -> bool:
    return all(isinstance(p, Path) and p.exists() and imghdr.what(p) for p in sequence)


class Image(VisionsBaseType):
    """**Image** implementation of :class:`visions.types.type.VisionsBaseType`.
    (i.e. series with all image files)

    Examples:
        >>> import visions
        >>> x = [Path('/home/user/file.png'), Path('/home/user/test2.jpg')]
        >>> x in visions.Image
        True
    """

    @classmethod
    def get_relations(cls) -> Sequence[TypeRelation]:
        from visions.types import File

        relations = [IdentityRelation(cls, File)]
        return relations

    @classmethod
    def contains_op(cls, sequence: Iterable, state: dict) -> bool:
        return image_contains(sequence, state)

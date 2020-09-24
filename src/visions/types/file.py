import pathlib
from functools import singledispatch
from typing import Iterable, Sequence

from visions.relations import IdentityRelation, TypeRelation
from visions.types.type import VisionsBaseType


@singledispatch
def file_contains(sequence: Iterable, state: dict) -> bool:
    return all(isinstance(p, pathlib.Path) and p.exists() for p in sequence)


class File(VisionsBaseType):
    """**File** implementation of :class:`visions.types.type.VisionsBaseType`.
    (i.e. existing path)

    Examples:
        >>> x = [pathlib.Path('/home/user/file.txt'), pathlib.Path('/home/user/test2.txt')]
        >>> x in visions.File
        True
    """

    @classmethod
    def get_relations(cls) -> Sequence[TypeRelation]:
        from visions.types import Path

        relations = [IdentityRelation(cls, Path)]
        return relations

    @classmethod
    def contains_op(cls, sequence: Iterable, state: dict) -> bool:
        return file_contains(sequence, state)

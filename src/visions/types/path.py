import pathlib
from functools import singledispatch
from typing import Iterable, Sequence

from visions.relations import IdentityRelation, InferenceRelation, TypeRelation
from visions.types.type import VisionsBaseType


@singledispatch
def string_is_path(series, state: dict) -> bool:
    try:
        s = string_to_path(series.copy(), state)
        return all(value.is_absolute() for value in s)
    except TypeError:
        return False


@singledispatch
def string_to_path(sequence: Iterable, state: dict) -> Iterable:
    s = map(sequence, pathlib.PureWindowsPath)
    if not all(value.is_absolute() for value in s):
        return map(sequence, pathlib.PurePosixPath)
    else:
        return s


@singledispatch
def path_contains(sequence: Iterable, state: dict) -> bool:
    return all(isinstance(x, pathlib.PurePath) and x.is_absolute() for x in sequence)


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
        from visions.types import Object, String

        relations = [
            IdentityRelation(cls, Object),
            InferenceRelation(
                cls, String, relationship=string_is_path, transformer=string_to_path
            ),
        ]
        return relations

    @classmethod
    def contains_op(cls, sequence: Iterable, state: dict) -> bool:
        return path_contains(sequence, state)

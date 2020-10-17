import pathlib
from typing import Sequence

from visions.types.path import Path
from visions.types.string import String


@Path.register_relationship(String, Sequence)
def string_is_path(series, state: dict) -> bool:
    try:
        s = string_to_path(series.copy(), state)
        return all(value.is_absolute() for value in s)
    except TypeError:
        return False


@Path.register_transformer(String, Sequence)
def string_to_path(sequence: Sequence, state: dict) -> Sequence:
    s = tuple(map(pathlib.PureWindowsPath, sequence))
    if not all(value.is_absolute() for value in s):
        return tuple(map(pathlib.PurePosixPath, sequence))
    else:
        return s


@Path.contains_op.register
def path_contains(sequence: Sequence, state: dict) -> bool:
    return all(isinstance(x, pathlib.PurePath) and x.is_absolute() for x in sequence)

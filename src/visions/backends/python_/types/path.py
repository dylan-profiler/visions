import pathlib
from typing import Iterable

from visions.types.path import Path
from visions.types.path import String


@Path.register_relationship(String, Iterable)
def string_is_path(series, state: dict) -> bool:
    try:
        s = string_to_path(series.copy(), state)
        return all(value.is_absolute() for value in s)
    except TypeError:
        return False


@Path.register_transformer(String, Iterable)
def string_to_path(sequence: Iterable, state: dict) -> Iterable:
    s = map(pathlib.PureWindowsPath, sequence)
    if not all(value.is_absolute() for value in s):
        return map(pathlib.PurePosixPath, sequence)
    else:
        return s


@Path.contains_op.register(Iterable)
def path_contains(sequence: Iterable, state: dict) -> bool:
    return all(isinstance(x, pathlib.PurePath) and x.is_absolute() for x in sequence)

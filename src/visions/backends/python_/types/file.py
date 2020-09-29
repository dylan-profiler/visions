import pathlib
from typing import Iterable

from visions.types.file import File


@File.contains_op.register(Iterable)
def file_contains(sequence: Iterable, state: dict) -> bool:
    return all(isinstance(p, pathlib.Path) and p.exists() for p in sequence)

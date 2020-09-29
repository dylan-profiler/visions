import imghdr
import pathlib
from typing import Iterable

from visions.types.image import Image


@Image.contains_op.register(Iterable)
def image_contains(sequence: Iterable, state: dict) -> bool:
    return all(
        isinstance(p, pathlib.Path) and p.exists() and imghdr.what(p) for p in sequence
    )

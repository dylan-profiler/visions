import pathlib
from typing import Sequence

import puremagic

from visions.types.image import Image


@Image.contains_op.register
def image_contains(sequence: Sequence, state: dict) -> bool:
    return all(
        isinstance(p, pathlib.Path) and p.exists() and puremagic.what(p) for p in sequence
    )

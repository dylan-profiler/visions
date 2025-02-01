import pathlib
from typing import Sequence

from visions.types.image import Image
from visions.utils.images.image_utils import path_is_image


@Image.contains_op.register
def image_contains(sequence: Sequence, state: dict) -> bool:
    return all(
        isinstance(p, pathlib.Path) and p.exists() and path_is_image(p)
        for p in sequence
    )

from visions.utils.images.image_utils import HAS_IMGHDR, HAS_PUREMAGIC
from visions.utils.monkeypatches import pathlib_patch

__all__ = [
    "pathlib_patch",
]

if HAS_IMGHDR and not HAS_PUREMAGIC:
    from visions.utils.monkeypatches import imghdr_patch

    __all__.append("imghdr_patch")

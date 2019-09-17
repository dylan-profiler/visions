from pathlib import Path
from typing import Union, Tuple
import imagehash
from PIL import Image, ExifTags
from tenzing.utils.monkeypatches.imghdr_patch import *
import imghdr


def open_image(path: Path) -> Image:
    """

    Args:
        path:

    Returns:

    """
    try:
        return Image.open(path)
    except (OSError, AttributeError) as err:
        return None


def is_image_truncated(image: Image) -> bool:
    """Returns True if the path refers to a truncated image

    Args:
        image:

    Returns:
        True if the image is truncated
    """
    try:
        image.load()
        return False
    except (OSError, AttributeError):
        return True


def get_image_shape(image: Image) -> Union[None, Tuple[int, int]]:
    """

    Args:
        image:

    Returns:

    """
    try:
        return image.size
    except (OSError, AttributeError):
        return None


def hash_image(image: Image) -> Union[str, None]:
    """

    Args:
        image:

    Returns:

    """
    try:
        return str(imagehash.phash(image))
    except (OSError, AttributeError):
        return None


def decode_byte_exif(exif_val):
    """Decode byte encodings

    Args:
        exif_val:

    Returns:

    """
    try:
        exif_val = exif_val.decode()
    except (UnicodeDecodeError, AttributeError):
        pass
    return exif_val


def extract_exif(image: Image) -> dict:
    """

    Args:
        image:

    Returns:

    """
    try:
        exif_data = image._getexif()
        if exif_data is not None:
            exif = {
                ExifTags.TAGS[k]: decode_byte_exif(v) for k, v in exif_data.items() if k in ExifTags.TAGS
            }
        else:
            exif = {}
    except (AttributeError, OSError):
        # Not all file types (e.g. .gif) have exif information.
        exif = {}

    return exif


def path_is_image(p: Path):
    return imghdr.what(p) is not None

from pathlib import Path
import pandas as pd

import imagehash
from PIL import Image, ExifTags


def is_image_truncated(image):
    """Returns True if the path refers to a truncated image

    Args:

    Returns:
        True if the image is truncated
    """
    try:
        image.load()
        return False
    except (OSError, AttributeError) as err:
        return True


def get_image_shape(image):
    try:
        return image.size
    except (OSError, AttributeError) as err:
        return None


def hash_image(image):
    try:
        return str(imagehash.phash(image))
    except (OSError, AttributeError) as err:
        return None


def count_duplicate_hashes(image_descriptions):
    counts = pd.Series(
        [x["hash"] for x in image_descriptions if "hash" in x]
    ).value_counts()
    return counts.sum() - len(counts)


def extract_exif(image):
    try:
        exif_data = image._getexif()
        if exif_data is not None:
            exif = {
                ExifTags.TAGS[k]: v for k, v in exif_data.items() if k in ExifTags.TAGS
            }
        else:
            exif = {}
    except (AttributeError, OSError):
        # Not all file types (e.g. .gif) have exif information.
        exif = {}

    return exif


def extract_exif_series(image_exifs):
    exif_keys = []
    exif_values = {}

    for image_exif in image_exifs:
        # Extract key
        exif_keys.extend(list(image_exif.keys()))

        # Extract values per key
        for exif_key, exif_val in image_exif.items():
            if exif_key not in exif_values:
                exif_values[exif_key] = []

            # Decode byte encodings
            try:
                exif_val = exif_val.decode()
            except (UnicodeDecodeError, AttributeError):
                pass

            exif_values[exif_key].append(exif_val)

    series = {"exif_keys": pd.Series(exif_keys).value_counts().to_dict()}

    for k, v in exif_values.items():
        series[k] = pd.Series(v).value_counts().to_dict()

    return series


def open_image(path: Path):
    try:
        return Image.open(path)
    except (OSError, AttributeError) as err:
        return None


def extract_image_information(path: Path):
    """Extracts all image information per file, as opening files is slow

    Args:
        path: Path to the image

    Returns:
        A dict containing image information
    """
    information = {}
    image = open_image(path)
    information["opened"] = image is not None
    if information["opened"]:
        information["truncated"] = is_image_truncated(image)
        if not information["truncated"]:
            information["size"] = image.size
            information["exif"] = extract_exif(image)
            information["hash"] = hash_image(image)
        # else:
        #     print(image.size)
    return information


def image_summary(series):
    image_information = series.apply(extract_image_information)
    summary = {"n_duplicate_hash": count_duplicate_hashes(image_information)}
    summary["p_duplicate_hash"] = float(summary["n_duplicate_hash"]) / len(series)

    summary["n_truncated"] = sum(
        [1 for x in image_information if "truncated" in x and x["truncated"]]
    )
    summary["p_truncated"] = float(summary["n_truncated"]) / len(series)

    exif_series = extract_exif_series(
        [x["exif"] for x in image_information if "exif" in x]
    )
    summary["exif_keys_counts"] = exif_series["exif_keys"]

    summary["scatter_data"] = pd.Series(
        [x["size"] for x in image_information if "size" in x], name="image_shape"
    )
    summary["image_shape_counts"] = summary["scatter_data"].value_counts().to_dict()

    return summary


def warnings(summary):
    messages = []
    if summary["n_truncated"] > 0:
        messages.append("n_truncated")
    return messages

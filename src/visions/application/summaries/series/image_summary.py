from pathlib import Path

import pandas as pd

from visions.utils.images.image_utils import (
    open_image,
    is_image_truncated,
    extract_exif,
    hash_image,
)


def count_duplicate_hashes(image_descriptions: dict) -> int:
    """

    Args:
        image_descriptions:

    Returns:

    """
    counts = pd.Series(
        [x["hash"] for x in image_descriptions if "hash" in x]
    ).value_counts()
    return counts.sum() - len(counts)


def extract_exif_series(image_exifs: list) -> dict:
    """

    Args:
        image_exifs:

    Returns:

    """
    exif_keys = []
    exif_values = {}

    for image_exif in image_exifs:
        # Extract key
        exif_keys.extend(list(image_exif.keys()))

        # Extract values per key
        for exif_key, exif_val in image_exif.items():
            if exif_key not in exif_values:
                exif_values[exif_key] = []

            exif_values[exif_key].append(exif_val)

    series = {"exif_keys": pd.Series(exif_keys).value_counts().to_dict()}

    for k, v in exif_values.items():
        series[k] = pd.Series(v).value_counts().to_dict()

    return series


def extract_image_information(path: Path) -> dict:
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


def image_summary(series: pd.Series) -> dict:
    """

    Args:
        series: series to summarize

    Returns:

    """
    image_information = series.apply(extract_image_information)
    summary = {
        "n_duplicate_hash": count_duplicate_hashes(image_information),
        "n_truncated": sum(
            [1 for x in image_information if "truncated" in x and x["truncated"]]
        ),
    }

    exif_series = extract_exif_series(
        [x["exif"] for x in image_information if "exif" in x]
    )
    summary["exif_keys_counts"] = exif_series["exif_keys"]

    image_shapes = pd.Series(
        [x["size"] for x in image_information if "size" in x], name="image_shape"
    )
    summary["image_shape_counts"] = image_shapes.value_counts().to_dict()

    return summary

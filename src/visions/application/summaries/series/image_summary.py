from functools import partial
from pathlib import Path

import pandas as pd

from visions.application.summaries.series.numerical_summary import (
    named_aggregate_summary,
)
from visions.utils.images.image_utils import (
    extract_exif,
    hash_image,
    is_image_truncated,
    open_image,
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
    exif_values: dict = {}

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
        series[k] = pd.Series(v).value_counts()

    return series


def extract_image_information(
    path: Path, exif: bool = False, hash: bool = False
) -> dict:
    """Extracts all image information per file, as opening files is slow

    Args:
        path: Path to the image
        exif: extract exif information
        hash: calculate hash (for duplicate detection)

    Returns:
        A dict containing image information
    """
    information: dict = {}
    image = open_image(path)
    information["opened"] = image is not None
    if image is not None:
        information["truncated"] = is_image_truncated(image)
        if not information["truncated"]:
            information["size"] = image.size
            if exif:
                information["exif"] = extract_exif(image)
            if hash:
                information["hash"] = hash_image(image)

    return information


def image_summary(series: pd.Series, exif: bool = False, hash: bool = False) -> dict:
    """

    Args:
        series: series to summarize
        exif: extract exif information
        hash: calculate hash (for duplicate detection)

    Returns:

    """

    image_information = series.apply(
        partial(extract_image_information, exif=exif, hash=hash)
    )
    summary = {
        "n_truncated": sum(
            [1 for x in image_information if "truncated" in x and x["truncated"]]
        ),
        "image_dimensions": pd.Series(
            [x["size"] for x in image_information if "size" in x],
            name="image_dimensions",
        ),
    }

    image_widths = summary["image_dimensions"].map(lambda x: x[0])
    summary.update(named_aggregate_summary(image_widths, "width"))
    image_heights = summary["image_dimensions"].map(lambda x: x[1])
    summary.update(named_aggregate_summary(image_heights, "height"))
    image_areas = image_widths * image_heights
    summary.update(named_aggregate_summary(image_areas, "area"))

    if hash:
        summary["n_duplicate_hash"] = count_duplicate_hashes(image_information)

    if exif:
        exif_series = extract_exif_series(
            [x["exif"] for x in image_information if "exif" in x]
        )
        summary["exif_keys_counts"] = exif_series["exif_keys"]
        summary["exif_data"] = exif_series

    return summary

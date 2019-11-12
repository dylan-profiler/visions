import os

import pandas as pd


def path_summary(series: pd.Series) -> dict:
    """

    Args:
        series: series to summarize

    Returns:

    """
    summary = {
        "common_prefix": (os.path.commonprefix(list(series)) or "No common prefix"),
        "stem_counts": series.map(lambda x: x.stem).value_counts().to_dict(),
        "suffix_counts": (series.map(lambda x: x.suffix).value_counts().to_dict()),
        "name_counts": series.map(lambda x: x.name).value_counts().to_dict(),
        "parent_counts": (series.map(lambda x: x.parent).value_counts().to_dict()),
        "anchor_counts": (series.map(lambda x: x.anchor).value_counts().to_dict()),
    }

    return summary

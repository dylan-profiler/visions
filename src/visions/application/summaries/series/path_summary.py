import os

import pandas as pd


def path_summary(series: pd.Series) -> dict:
    """

    Args:
        series: series to summarize

    Returns:

    """
    summary = {
        "common_prefix": os.path.commonprefix(list(series)) or "No common prefix",
        "stem_counts": series.map(lambda x: x.stem).value_counts(),
        "suffix_counts": series.map(lambda x: x.suffix).value_counts(),
        "name_counts": series.map(lambda x: x.name).value_counts(),
        "parent_counts": series.map(lambda x: x.parent).value_counts(),
        "anchor_counts": series.map(lambda x: x.anchor).value_counts(),
    }

    summary["n_stem_unique"] = len(summary["stem_counts"])
    summary["n_suffix_unique"] = len(summary["suffix_counts"])
    summary["n_name_unique"] = len(summary["name_counts"])
    summary["n_parent_unique"] = len(summary["parent_counts"])
    summary["n_anchor_unique"] = len(summary["anchor_counts"])

    return summary

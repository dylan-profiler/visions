import numpy as np
import pandas as pd


def infinite_summary(series: pd.Series) -> dict:
    """Counts the number of infinite values.

    Args:
        series: series to summarize

    Returns:
        A dict containing `inf_count`.
    """
    summary = {}
    mask = (~np.isfinite(series)) & series.notnull()
    summary["inf_count"] = mask.values.sum()
    return summary

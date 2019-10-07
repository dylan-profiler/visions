import numpy as np
import pandas as pd


def infinite_summary(series: pd.Series) -> dict:
    """

    Args:
        series:

    Returns:

    """
    summary = {}
    mask = (~np.isfinite(series)) & series.notnull()
    summary["inf_count"] = mask.values.sum()
    return summary

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
    summary["perc_inf"] = (
        summary["inf_count"] / series.shape[0] if series.shape[0] > 0 else np.nan
    )
    return summary

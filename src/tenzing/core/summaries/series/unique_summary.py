import numpy as np
import pandas as pd


def unique_summary(series: pd.Series) -> dict:
    """

    Args:
        series:

    Returns:

    """
    summary = {}

    # try:
    # n_unique = len(set(series.values))
    n_unique = series.nunique()
    summary.update({"n_unique": n_unique})
    # except Exception:
    #     pass
    return summary

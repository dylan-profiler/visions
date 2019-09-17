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
    n_unique = len(set(series.values))
    # n_unique = series.nunique()
    summary.update(
        {
            "n_unique": n_unique,
            "perc_unique": float(n_unique) / len(series) if len(series) > 0 else np.nan,
        }
    )
    # except Exception:
    #     pass
    return summary



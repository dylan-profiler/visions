import numpy as np
import pandas as pd


def zero_summary(series: pd.Series) -> dict:
    """

    Args:
        series:

    Returns:

    """
    summary = {"n_zeros": (series == 0).sum()}
    summary["perc_zeros"] = (
        summary["n_zeros"] / len(series) if len(series) > 0 else np.nan
    )
    return summary

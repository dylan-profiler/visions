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


def zero_warnings(summary: dict) -> list:
    """

    Args:
        summary:

    Returns:

    """
    messages = []
    if summary["n_unique"] == 1:
        messages.append("n_unique:const")
    if summary["p_unique"] == 1.0:
        messages.append("n_unique:unique")
    return messages

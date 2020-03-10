import pandas as pd


def zero_summary(series: pd.Series) -> dict:
    """

    Args:
        series: series to summarize

    Returns:

    """
    summary = {"n_zeros": (series == 0).sum()}
    return summary

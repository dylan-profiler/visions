import numpy as np
import pandas as pd


def unique_summary(series: pd.Series) -> dict:
    """

    Args:
        series: series to summarize

    Returns:

    """
    summary = {}
    summary.update({"n_unique": series.nunique()})
    return summary


def unique_summary_complex(series: pd.Series) -> dict:
    """

    Args:
        series: series to summarize

    Returns:

    """
    summary = {}
    # Until complex bug is fixed:
    # https://github.com/pandas-dev/pandas/issues/17927
    # https://github.com/pandas-dev/pandas/pull/27599
    n_unique = len(set(series[series.notna()].values))
    summary.update({"n_unique": n_unique})
    return summary

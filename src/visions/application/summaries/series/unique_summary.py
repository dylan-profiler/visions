import pandas as pd


def unique_summary(series: pd.Series) -> dict:
    """

    Args:
        series: series to summarize

    Returns:

    """
    summary = {"n_unique": series.nunique(), "is_unique": series.is_unique}
    return summary


def unique_summary_complex(series: pd.Series) -> dict:
    """

    Args:
        series: series to summarize

    Notes:
        Until complex bug is fixed:
        - https://github.com/pandas-dev/pandas/issues/17927
        - https://github.com/pandas-dev/pandas/pull/27599

    Returns:

    """

    n_unique = len(set(series[series.notna()].values))
    summary = {"n_unique": n_unique, "is_unique": series.is_unique}
    return summary

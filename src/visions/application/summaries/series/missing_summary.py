import pandas as pd


def missing_summary(series: pd.Series) -> dict:
    """Counts the number of missing values

    Args:
        series: series to summarize

    Returns:
        A dict containing `na_count`.
    """
    mask = series.isna()
    summary = {"na_count": mask.values.sum()}
    return summary

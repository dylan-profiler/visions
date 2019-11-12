import pandas as pd


def existing_path_summary(series: pd.Series) -> dict:
    """

    Args:
        series: series to summarize

    Returns:

    """
    summary = {"file_sizes": series.map(lambda x: x.stat().st_size)}
    return summary

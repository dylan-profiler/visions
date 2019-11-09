import pandas as pd


def range_summary(series: pd.Series) -> dict:
    """

    Args:
        series:

    Returns:

    """
    aggregates = ["min", "max"]
    summary = series.agg(aggregates).to_dict()

    summary["range"] = summary["max"] - summary["min"]
    return summary

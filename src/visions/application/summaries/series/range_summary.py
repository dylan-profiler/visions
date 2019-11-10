import pandas as pd


def range_summary(series: pd.Series) -> dict:
    """Summarize min, max and calculate the range

    Args:
        series: series to summarize

    Returns:
        A dict with `min`, `max` and `range`.
    """
    aggregates = ["min", "max"]
    summary = series.agg(aggregates).to_dict()

    summary["range"] = summary["max"] - summary["min"]
    return summary

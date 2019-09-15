import pandas as pd


# TODO: rename to reflect contents of summary and promote reuse
def complex_summary(series: pd.Series) -> dict:
    """Summary with basic aggregates

    Args:
        series: series to summarize

    Returns:
        A summary of aggregates of `mean`, `std`, `var`, `min`, `max` and `sum`.

    """
    aggregates = ["mean", "std", "var", "min", "max", "sum"]
    summary = series.agg(aggregates).to_dict()
    return summary

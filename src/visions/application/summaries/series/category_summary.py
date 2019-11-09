import pandas as pd


def category_summary(series: pd.Series) -> dict:
    """Summary for pandas.Categorical

    Args:
        series: series to summarize

    Returns:
        A summary of the series including `category_size`, `ordered` and `missing_categorical_values`.
    """
    summary = {
        "category_size": len(series.dtype._categories),
        "ordered": series.dtype.ordered,
    }

    summary["missing_categorical_values"] = (
        True if series.nunique() != summary["category_size"] else False
    )
    return summary

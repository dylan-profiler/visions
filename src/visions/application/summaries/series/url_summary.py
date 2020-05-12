import pandas as pd


def url_summary(series: pd.Series) -> dict:
    """

    Args:
        series: series to summarize

    Returns:

    """
    summary = {
        "scheme_counts": series.map(lambda x: x.scheme).value_counts(),
        "netloc_counts": series.map(lambda x: x.netloc).value_counts(),
        "path_counts": series.map(lambda x: x.path).value_counts(),
        "query_counts": series.map(lambda x: x.query).value_counts(),
        "fragment_counts": series.map(lambda x: x.fragment).value_counts(),
    }

    return summary

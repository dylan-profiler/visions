# TODO: percentages
# TODO: rename to aggregate?


def dataframe_series_summary(series_summaries: dict) -> dict:
    """Aggregate certain statistics from the series summary

    Args:
        series_summaries: mapping from series to summary

    Returns:
        A aggregated summary based on the statistics of individual series
    """
    summary = {"na_count": 0, "n_vars_missing": 0}
    for series_summary in series_summaries.values():
        if "na_count" in series_summary and series_summary["na_count"] > 0:
            summary["na_count"] += series_summary["na_count"]
    return summary

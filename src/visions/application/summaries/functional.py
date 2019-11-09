import pandas as pd

from visions.core.model import VisionsBaseType
from visions.application.summaries.summary import Summary


def summarize_frame(df: pd.DataFrame, series_types: dict, summarizer: Summary):
    return summarizer.summarize_frame(df, {}, series_types)


def summarize_series(
    series: pd.Series, series_type: VisionsBaseType, summarizer: Summary
):
    return summarizer.summarize_series(series, series_type)


def summarize(df: pd.DataFrame, series_types: dict, summarizer: Summary):
    return summarizer.summarize(df, series_types)

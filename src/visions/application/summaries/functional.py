from typing import Type

import pandas as pd

from visions.application.summaries.summary import Summary
from visions.types import VisionsBaseType


def summarize_frame(df: pd.DataFrame, series_types: dict, summarizer: Summary) -> dict:
    return summarizer.summarize_frame(df, {}, series_types)


def summarize_series(
    series: pd.Series, series_type: Type[VisionsBaseType], summarizer: Summary
) -> dict:
    return summarizer.summarize_series(series, series_type)


def summarize(df: pd.DataFrame, series_types: dict, summarizer: Summary) -> dict:
    return summarizer.summarize(df, series_types)

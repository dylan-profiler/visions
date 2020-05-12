from datetime import datetime

import pandas as pd


def file_summary(series: pd.Series) -> dict:
    """

    Args:
        series: series to summarize

    Returns:

    """

    stats = series.map(lambda x: x.stat())

    def convert_datetime(x):
        return datetime.fromtimestamp(x).strftime("%Y-%m-%d %H:%M:%S")

    summary = {
        "file_size": stats.map(lambda x: x.st_size),
        "file_created_time": stats.map(lambda x: x.st_ctime).map(convert_datetime),
        "file_accessed_time": stats.map(lambda x: x.st_atime).map(convert_datetime),
        "file_modified_time": stats.map(lambda x: x.st_mtime).map(convert_datetime),
    }
    return summary

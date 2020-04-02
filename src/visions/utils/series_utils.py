from typing import Callable

import pandas as pd


def nullable_series_contains(fn: Callable) -> Callable:
    def inner(cls, series: pd.Series) -> bool:
        if series.hasnans:
            series = series.dropna()
            if series.empty:
                return False

        return fn(cls, series)

    return inner

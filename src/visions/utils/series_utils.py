from typing import Callable

import pandas as pd


def nullable_series_contains(fn: Callable) -> Callable:
    def inner(cls, series: pd.Series, *args, **kwargs) -> bool:
        if series.hasnans:
            series = series.dropna()
            if series.empty:
                return False

        return fn(cls, series, *args, **kwargs)

    return inner


def func_nullable_series_contains(fn: Callable) -> Callable:
    def inner(series: pd.Series, *args, **kwargs) -> bool:
        if series.hasnans:
            series = series.dropna()
            if series.empty:
                return False

        return fn(series, *args, **kwargs)

    return inner


def isinstance_attrs(series, class_name, attrs: list, sample_size=1):
    # TODO: user configurable .head or .sample
    # TODO: performance testing for series[0], series.iloc[0], series.head, series.sample
    if not all(isinstance(x, class_name) for x in series.head(sample_size)):
        return False

    try:
        return all(all(hasattr(x, attr) for attr in attrs) for x in series)
    except AttributeError:
        return False

import functools
from typing import Callable

import pandas as pd
from pandas.api import types as pdt

# For future reference: get the dtype from the subtype when the series is sparse
# def sparse_series_contains(fn: Callable):
#     @functools.wraps(fn)
#     def inner(cls, series: pd.Series, *args, **kwargs) -> bool:
#         if pdt.is_sparse(series):
#             dtype = series.dtype.subtype
#         else:
#             dtype = series.dtype
#         # TODO: pass dtype (e.g. in state)
#
#         return fn(cls, series, *args, **kwargs)
#     return inner


def nullable_series_contains(fn: Callable) -> Callable:
    @functools.wraps(fn)
    def inner(cls, series: pd.Series, state: dict = {}, *args, **kwargs) -> bool:
        if series.hasnans:
            series = series.dropna()
            if series.empty:
                return False

        return fn(cls, series, state, *args, **kwargs)

    return inner


def func_nullable_series_contains(fn: Callable) -> Callable:
    @functools.wraps(fn)
    def inner(series: pd.Series, state={}, *args, **kwargs) -> bool:
        if series.hasnans:
            series = series.dropna()
            if series.empty:
                return False

        return fn(series, state, *args, **kwargs)

    return inner


def series_not_sparse(fn: Callable) -> Callable:
    @functools.wraps(fn)
    def inner(cls, series: pd.Series, *args, **kwargs) -> bool:
        if pdt.is_sparse(series):
            return False
        return fn(cls, series, *args, **kwargs)

    return inner


def series_not_empty(fn: Callable) -> Callable:
    @functools.wraps(fn)
    def inner(cls, series: pd.Series, *args, **kwargs) -> bool:
        if series.empty:
            return False
        return fn(cls, series, *args, **kwargs)

    return inner


def _contains_instance_attrs(
    series, is_method, class_name, attrs: list, sample_size=1
) -> bool:
    # TODO: user configurable .head or .sample
    # TODO: performance testing for series[0], series.iloc[0], series.head, series.sample
    if not all(is_method(x, class_name) for x in series.head(sample_size)):
        return False

    try:
        return all(all(hasattr(x, attr) for attr in attrs) for x in series)
    except AttributeError:
        return False


def class_name_attrs(series, class_name, attrs: list, sample_size=1) -> bool:
    def func(instance, class_name):
        return instance.__class__.__name__ == class_name.__name__

    return _contains_instance_attrs(series, func, class_name, attrs, sample_size)


def isinstance_attrs(series, class_name, attrs: list, sample_size=1) -> bool:
    return _contains_instance_attrs(series, isinstance, class_name, attrs, sample_size)

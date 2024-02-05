import functools
from typing import Callable

import pandas as pd


# For future reference: get the dtype from the subtype when the series is sparse
def series_handle_sparse_dtype(fn: Callable[..., bool]) -> Callable[..., bool]:
    """Decorator to include the dtype of a sparse subtype."""

    @functools.wraps(fn)
    def inner(series: pd.Series, state: dict, *args, **kwargs) -> bool:
        if isinstance(series.dtype, pd.SparseDtype):
            dtype = series.dtype.subtype
        else:
            dtype = series.dtype
        state["dtype"] = dtype

        return fn(series, state, *args, **kwargs)

    return inner


def series_handle_nulls(fn: Callable[..., bool]) -> Callable[..., bool]:
    """Decorator for nullable series"""

    @functools.wraps(fn)
    def inner(series: pd.Series, *args, **kwargs) -> bool:
        if series.hasnans:
            series = series.dropna()
            # TODO: use series_not_empty?
            if series.empty:
                return False

        return fn(series, *args, **kwargs)

    return inner


def series_not_sparse(fn: Callable[..., bool]) -> Callable[..., bool]:
    """Decorator to exclude sparse series"""

    @functools.wraps(fn)
    def inner(series: pd.Series, *args, **kwargs) -> bool:
        if isinstance(series, pd.SparseDtype):
            return False
        return fn(series, *args, **kwargs)

    return inner


def series_not_empty(fn: Callable[..., bool]) -> Callable[..., bool]:
    """Decorator to exclude empty series"""

    @functools.wraps(fn)
    def inner(series: pd.Series, *args, **kwargs) -> bool:
        if series.empty:
            return False
        return fn(series, *args, **kwargs)

    return inner


# TODO: What is the type signature on is_method????
def _contains_instance_attrs(
    series: pd.Series, is_method, class_name: str, attrs: list, sample_size: int = 1
) -> bool:
    # TODO: user configurable .head or .sample
    # TODO: performance testing for series[0], series.iloc[0], series.head, series.sample
    if not all(is_method(x, class_name) for x in series.head(sample_size)):
        return False

    try:
        return all(all(hasattr(x, attr) for attr in attrs) for x in series)
    except AttributeError:
        return False


# TODO: What is the type signature on class_name????
def class_name_attrs(
    series: pd.Series, class_name, attrs: list, sample_size: int = 1
) -> bool:
    def func(instance, class_name):
        return instance.__class__.__name__ == class_name.__name__

    return _contains_instance_attrs(series, func, class_name, attrs, sample_size)


# TODO: What is the type signature on class_name????
def isinstance_attrs(
    series: pd.Series, class_name, attrs: list, sample_size: int = 1
) -> bool:
    return _contains_instance_attrs(series, isinstance, class_name, attrs, sample_size)

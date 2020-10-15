"""
A selection of testing utilities for visions.
"""
import functools
from typing import Callable, Dict, List, Optional, Type, Union

import pandas as pd

from visions.backends.pandas.series_utils import series_handle_nulls

pandas_version = tuple([int(i) for i in pd.__version__.split(".")])
pandas_na_value = pd.NA if hasattr(pd, "NA") else None


def option_coercion_evaluator(
    fn: Callable[[pd.Series], pd.Series],
    extra_errors: Optional[List[Type[Exception]]] = None,
) -> Callable[[pd.Series], Optional[pd.Series]]:
    """A coercion test evaluator
    Evaluates a coercion function and optionally returns the coerced series.
    Args:
        fn: A function coercing a Series to another Series.
        extra_errors: Additional exceptions to catch
    Returns:
        The coerced series if the coercion succeeds otherwise None.
    """

    error_list = [ValueError, TypeError, AttributeError]
    if extra_errors:
        error_list.extend(extra_errors)

    @functools.wraps(fn)
    def f(series: pd.Series) -> Optional[pd.Series]:
        try:
            return fn(series)
        except tuple(error_list):
            return None

    return f


def coercion_test(
    fn: Callable[[pd.Series], pd.Series],
    extra_errors: Optional[List[Type[Exception]]] = None,
) -> Callable[[pd.Series], bool]:
    """A coercion test generator
    Creates a coercion test based on a provided coercion function.
    Args:
        fn: A function coercing a Series to another type.
        extra_errors: Additional exceptions to catch
    Returns:
        Whether the coercion failed or was successful.
    """
    # Returns True or False if the coercion succeeds
    tester = option_coercion_evaluator(fn, extra_errors)

    @functools.wraps(fn)
    def f(series: pd.Series) -> bool:
        result = tester(series)
        return True if result is not None else False

    return f


def coercion_true_test(
    fn: Callable[[pd.Series], pd.Series],
    extra_errors: Optional[List[Type[Exception]]] = None,
) -> Callable[[pd.Series], bool]:
    """A coercion equality test generator
    Creates a coercion test based on a provided coercion function which also enforces
    equality constraints on the output. This is useful when you want to change the
    data type of a series without necessarily changing the data, for example,
    when converting an integer to a float.
    Args:
        fn: A function coercing a Series to another type.
        extra_errors: Additional exceptions to catch
    Returns:
        Whether the coercion failed or was successful.
    """
    tester = option_coercion_evaluator(fn, extra_errors)

    @functools.wraps(tester)
    def f(series: pd.Series) -> bool:
        result = tester(series)
        return False if result is None else series.all()

    return f


def coercion_equality_test(
    fn: Callable[[pd.Series], pd.Series]
) -> Callable[[pd.Series], bool]:
    """A coercion equality test generator
    Creates a coercion test based on a provided coercion function which also enforces
    equality constraints on the output. This is useful when you want to change the
    data type of a series without necessarily changing the data, for example,
    when converting an integer to a float.
    Args:
        fn: A function coercing a Series to another type.
    Returns:
        Whether the coercion failed or was successful.
    """
    tester = option_coercion_evaluator(fn)

    @functools.wraps(tester)
    def f(series: pd.Series) -> bool:
        result = tester(series)
        return False if result is None else series.eq(result).all()

    return f


def coercion_single_map_test(mapping: List[Dict]) -> Callable[[pd.Series, Dict], bool]:
    @series_handle_nulls
    def f(series: pd.Series, state: dict = {}) -> bool:
        return any(series.isin(list(single_map.keys())).all() for single_map in mapping)

    return f


def coercion_multi_map_test(mapping: Dict) -> Callable[[pd.Series, Dict], bool]:
    @series_handle_nulls
    def f(series: pd.Series, state: dict = {}) -> bool:
        return series.isin(list(mapping.keys())).all()

    return f


def coercion_map_test(
    mapping: Union[List[Dict], Dict]
) -> Callable[[pd.Series, Dict], bool]:
    """Create a testing function for a single mapping or a list of mappings.
    Args:
        mapping: A dict with a mapping or a list of dicts
    Returns:
        Callable that checks if a series consists of the mappable values
    Examples:
        >>> coercion_map_test({"Yes": True, "No": False})
        >>> coercion_map_test(
        >>>     [
        >>>         {"Yes": True, "No": False},
        >>>         {"Y": True, "N": False},
        >>>     ]
        >>> )
    """

    if isinstance(mapping, list):
        f = coercion_single_map_test(mapping)
    elif isinstance(mapping, dict):
        f = coercion_multi_map_test(mapping)
    else:
        raise ValueError("Mapping should be dict or list of dicts")
    return f


def coercion_map(mapping: Union[List[Dict], Dict]) -> Callable[[pd.Series], pd.Series]:
    """Maps a series given a mapping
    Args:
        mapping: a dict to map, or a list of dicts.
    Returns:
        A callable that maps the series.
    """
    if type(mapping) == list:
        mapping = {k: v for d in mapping for k, v in d.items()}

    elif type(mapping) != dict:
        raise ValueError("Mapping should be dict or list of dicts")

    def f(series: pd.Series) -> pd.Series:
        return series.map(mapping)

    return f

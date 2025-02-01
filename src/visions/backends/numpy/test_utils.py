"""
A selection of testing utilities for visions.
"""

import functools
from typing import Callable, Dict, List, Optional, Type, Union

import numpy as np

from visions.backends.numpy.array_utils import array_handle_nulls


def option_coercion_evaluator(
    fn: Callable[[np.ndarray], np.ndarray],
    extra_errors: Optional[List[Type[Exception]]] = None,
) -> Callable[[np.ndarray], Optional[np.ndarray]]:
    """A coercion test evaluator
    Evaluates a coercion function and optionally returns the coerced array.
    Args:
        fn: A function coercing a array to another array.
        extra_errors: Additional exceptions to catch
    Returns:
        The coerced array if the coercion succeeds otherwise None.
    """

    error_list = [ValueError, TypeError, AttributeError]
    if extra_errors:
        error_list.extend(extra_errors)

    @functools.wraps(fn)
    def f(array: np.ndarray) -> Optional[np.ndarray]:
        try:
            return fn(array)
        except tuple(error_list):
            return None

    return f


def coercion_test(
    fn: Callable[[np.ndarray], np.ndarray],
    extra_errors: Optional[List[Type[Exception]]] = None,
) -> Callable[[np.ndarray], bool]:
    """A coercion test generator
    Creates a coercion test based on a provided coercion function.
    Args:
        fn: A function coercing a array to another type.
        extra_errors: Additional exceptions to catch
    Returns:
        Whether the coercion failed or was successful.
    """
    # Returns True or False if the coercion succeeds
    tester = option_coercion_evaluator(fn, extra_errors)

    @functools.wraps(fn)
    def f(array: np.ndarray) -> bool:
        result = tester(array)
        return True if result is not None else False

    return f


def coercion_true_test(
    fn: Callable[[np.ndarray], np.ndarray],
    extra_errors: Optional[List[Type[Exception]]] = None,
) -> Callable[[np.ndarray], bool]:
    """A coercion equality test generator
    Creates a coercion test based on a provided coercion function which also enforces
    equality constraints on the output. This is useful when you want to change the
    data type of a array without necessarily changing the data, for example,
    when converting an integer to a float.
    Args:
        fn: A function coercing a array to another type.
        extra_errors: Additional exceptions to catch
    Returns:
        Whether the coercion failed or was successful.
    """
    tester = option_coercion_evaluator(fn, extra_errors)

    @functools.wraps(tester)
    def f(array: np.ndarray) -> bool:
        result = tester(array)
        return False if result is None else array.all()

    return f


def coercion_equality_test(
    fn: Callable[[np.ndarray], np.ndarray],
) -> Callable[[np.ndarray], bool]:
    """A coercion equality test generator
    Creates a coercion test based on a provided coercion function which also enforces
    equality constraints on the output. This is useful when you want to change the
    data type of a array without necessarily changing the data, for example,
    when converting an integer to a float.
    Args:
        fn: A function coercing a array to another type.
    Returns:
        Whether the coercion failed or was successful.
    """
    tester = option_coercion_evaluator(fn)

    @functools.wraps(tester)
    def f(array: np.ndarray) -> bool:
        result = tester(array)
        return False if result is None else np.array_equal(array, result)

    return f


def coercion_single_map_test(mapping: List[Dict]) -> Callable[[np.ndarray, Dict], bool]:
    @array_handle_nulls
    def f(array: np.ndarray, state: dict = {}) -> bool:
        return any(
            np.isin(array, list(single_map.keys())).all() for single_map in mapping
        )

    return f


def coercion_multi_map_test(mapping: Dict) -> Callable[[np.ndarray, Dict], bool]:
    @array_handle_nulls
    def f(array: np.ndarray, state: dict = {}) -> bool:
        return np.isin(array, list(mapping.keys())).all()

    return f


def coercion_map_test(
    mapping: Union[List[Dict], Dict],
) -> Callable[[np.ndarray, Dict], bool]:
    """Create a testing function for a single mapping or a list of mappings.
    Args:
        mapping: A dict with a mapping or a list of dicts
    Returns:
        Callable that checks if a array consists of the mappable values
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


def coercion_map(
    mapping: Union[List[Dict], Dict],
) -> Callable[[np.ndarray], np.ndarray]:
    """Maps a array given a mapping
    Args:
        mapping: a dict to map, or a list of dicts.
    Returns:
        A callable that maps the array.
    """
    if isinstance(mapping, list):
        mapping = {k: v for d in mapping for k, v in d.items()}
    elif not isinstance(mapping, dict):
        raise ValueError("Mapping should be dict or list of dicts")

    f = np.vectorize(lambda value: mapping.get(value, np.nan))

    return f

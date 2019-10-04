"""
A selection of testing utilities for tenzing.
"""
from typing import Callable, Optional
import pandas as pd


def option_coercion_evaluator(method: Callable) -> Callable:
    """A coercion test evaluator

    Evaluates a coercion method and optionally returns the coerced series.

    Args:
        method: A method coercing a Series to another Series.

    Returns:
        The coerced series if the coercion succeeds otherwise None.
    """

    def f(series: pd.Series) -> Optional[pd.Series]:
        try:
            return method(series)
        except (ValueError, TypeError, AttributeError):
            return None

    return f


def coercion_test(method: Callable) -> Callable:
    """A coercion test generator

    Creates a coercion test based on a provided coercion method.

    Args:
        method: A method coercing a Series to another type.

    Returns:
        Whether the coercion failed or was successful.

    """
    # Returns True or False if the coercion succeeds
    tester = option_coercion_evaluator(method)

    def f(series: pd.Series) -> bool:
        result = tester(series)
        return True if result is not None else False

    return f


def coercion_equality_test(method: Callable) -> Callable:
    """A coercion equality test generator

    Creates a coercion test based on a provided coercion method which also enforces
    equality constraints on the output. This is useful when you want to change the
    data type of a series without necessarily changing the data, for example,
    when converting an integer to a float.

    Args:
        method: A method coercing a Series to another type.

    Returns:
        Whether the coercion failed or was successful.
    """
    tester = option_coercion_evaluator(method)

    def f(series: pd.Series) -> bool:
        result = tester(series)
        return False if result is None else series.eq(result).all()

    return f

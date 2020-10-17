import functools
import os
import sys
import warnings
from typing import Callable, TypeVar

T = TypeVar("T")


def suppress_warnings(func: Callable[..., T]) -> Callable[..., T]:
    """Suppress warnings produces while executing the wrapped function."""

    @functools.wraps(func)
    def inner(*args, **kwargs) -> T:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            return func(*args, **kwargs)

    return inner


def discard_stderr(func: Callable[..., T]) -> Callable[..., T]:
    """Shapely logs failures at a silly severity, just trying to suppress it's output on failures.
    Only known way to get rid of sys output when wkt.loads hits a bad value"""

    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> T:
        sys.stderr = open(os.devnull, "w")
        res = func(*args, **kwargs)
        sys.stderr = sys.__stderr__
        return res

    return wrapper

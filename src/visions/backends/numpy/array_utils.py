import functools
from typing import Callable

import numpy as np

from visions.backends.shared.nan_handling import nan_mask


def array_handle_nulls(fn: Callable[..., bool]) -> Callable[..., bool]:
    """Decorator for nullable arrays"""

    handles_missing = array_not_empty(fn)

    @functools.wraps(fn)
    def inner(array: np.ndarray, *args, **kwargs) -> bool:
        array = array[nan_mask(array)]
        return handles_missing(array, *args, **kwargs)

    return inner


def array_not_empty(fn: Callable[..., bool]) -> Callable[..., bool]:
    """Decorator to exclude empty arrays"""

    @functools.wraps(fn)
    def inner(array: np.ndarray, *args, **kwargs) -> bool:
        if array.shape[0] == 0:
            return False
        return fn(array, *args, **kwargs)

    return inner

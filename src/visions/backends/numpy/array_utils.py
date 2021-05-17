import functools
from typing import Callable

import numpy as np
import numba as nb
import math


@nb.njit
def anynan(array):
    array = array.ravel()
    for i in range(array.size):
        if math.isnan(array[i]):
            return True
    return False


def array_handle_nulls(fn: Callable[..., bool]) -> Callable[..., bool]:
    """Decorator for nullable arrays"""

    handles_missing = array_not_empty(fn)
    @functools.wraps(fn)
    def inner(array: np.ndarray, *args, **kwargs) -> bool:
        try:
            mask = np.isnan(array)
        except TypeError:
            # TODO: Fails for values like None, pandas resolves this but it's complicated some links:
            # https://github.com/pandas-dev/pandas/blob/3391a348f3f7cd07a96c8e6a4b05e3e9f60c8567/pandas/core/series.py#L192
            # https://github.com/pandas-dev/pandas/blob/65319af6e563ccbb02fb5152949957b6aef570ef/pandas/core/base.py#L816
            # https://github.com/pandas-dev/pandas/blob/65319af6e563ccbb02fb5152949957b6aef570ef/pandas/core/dtypes/missing.py#L133
            # https://github.com/pandas-dev/pandas/blob/65319af6e563ccbb02fb5152949957b6aef570ef/pandas/core/dtypes/missing.py#L202
            #raise NotImplementedError('Robust missing value detection not implemented for numpy arrays')
            nans = set([None, np.nan])
            def nan_check(v):
                try:
                    return v in nans
                except:
                    return False
            mask = np.array([nan_check(v) for v in array], dtype=bool)

        if mask.any():
            array = array[mask]
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







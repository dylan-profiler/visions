import functools
from typing import Callable, Sequence, Tuple, TypeVar, Union

import numpy as np

from visions.backends.shared.nan_handling import nan_mask
from visions.backends.shared.utilities import has_import

has_numba = has_import("numba")

if has_numba:
    import numba as nb

T = TypeVar("T")


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


def _base_all_type(array: np.ndarray, dtypes: Union[type, Tuple[type, ...]]) -> bool:
    return all(isinstance(v, dtypes) for v in array)


if has_numba:
    # TODO: This only works when the numpy array dtype falls under a few categories
    # There are alternative implementations with forceobj=True which work in all cases
    # including the use of isinstance, but in those cases worst case performance can be substantially worse
    # than the default python implementation.
    def all_type_numba(dtype: Union[Tuple, T]):
        @nb.jit(nopython=True)
        def inner(array: np.ndarray) -> bool:
            for i in nb.prange(array.size):
                if type(array[i]) is not dtype:
                    return False
            return True

        return inner

    def all_type(array: np.ndarray, dtypes: Union[type, Tuple[type, ...]]) -> bool:
        return _base_all_type(array, dtypes)

else:

    def all_type(array: np.ndarray, dtypes: Union[type, Tuple[type, ...]]) -> bool:
        return _base_all_type(array, dtypes)

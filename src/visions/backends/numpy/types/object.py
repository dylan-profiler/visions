from datetime import datetime

import numpy as np

from visions.backends.numpy.array_utils import (array_handle_nulls,
                                                array_not_empty)
from visions.types.object import Object


def not_excluded_type(array: np.ndarray, excludes) -> bool:

    if len(array) == 0 or not isinstance(array[0], excludes):
        return True

    dtype = type(array[0])
    return not all(isinstance(v, dtype) for v in array)


@Object.contains_op.register
@array_handle_nulls
@array_not_empty
def object_contains(array: np.ndarray, state: dict) -> bool:
    if not np.issubdtype(array.dtype, np.object_):
        return False

    return not_excluded_type(array, (bool, int, datetime))

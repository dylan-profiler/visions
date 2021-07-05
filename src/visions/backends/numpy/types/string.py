import numpy as np

from visions.backends.numpy.array_utils import array_handle_nulls, array_not_empty
from visions.types.string import String


@array_handle_nulls
def _is_string(array: np.ndarray, state: dict):
    if not all(isinstance(v, str) for v in array[0:5]):
        return False
    try:
        return (array.astype(str) == array).all()
    except (TypeError, ValueError):
        return False


@String.contains_op.register
@array_not_empty
def string_contains(array: np.ndarray, state: dict) -> bool:
    if np.issubdtype(array.dtype, np.str_):
        return True

    return _is_string(array, state)

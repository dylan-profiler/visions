import numpy as np

from visions.backends.numpy.array_utils import (
    array_handle_nulls,
    array_not_empty,
)
from visions.types.object import Object


@Object.contains_op.register
@array_handle_nulls
@array_not_empty
def object_contains(array: np.ndarray, state: dict) -> bool:
    return np.issubdtype(array.dtype, object) or np.issubdtype(array.dtype, str)

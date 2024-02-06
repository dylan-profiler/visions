import numpy as np

from visions.backends.numpy.array_utils import array_handle_nulls
from visions.types.float import Float
from visions.types.integer import Integer


@Integer.register_relationship(Float, np.ndarray)
def float_is_integer(series: np.ndarray, state: dict) -> bool:
    return np.all(np.mod(series[~np.isnan(series)], 1) == 0)


# TODO: The array_handle_nulls is actually removing nulls from the result. This is _far_ from ideal but there is no
# other native way to represent nullable integers in numpy
@Integer.register_transformer(Float, np.ndarray)
@array_handle_nulls
def float_to_integer(series: np.ndarray, state: dict) -> np.ndarray:
    return series.astype(int)


@Integer.contains_op.register
@array_handle_nulls
def integer_contains(sequence: np.ndarray, state: dict) -> bool:
    if sequence.shape[0] == 0 or np.issubdtype(sequence.dtype, np.timedelta64):
        return False
    elif np.issubdtype(sequence.dtype, np.integer):
        return True
    elif np.issubdtype(sequence.dtype, np.object_):
        return all(isinstance(v, int) and not isinstance(v, bool) for v in sequence)

    return False

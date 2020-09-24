import numpy as np

from visions.types.integer import float_is_int, float_to_int, integer_contains


@float_to_int.register(np.ndarray)
def _(series: np.ndarray, state: dict) -> np.ndarray:
    return series.astype(np.int)


@float_is_int.register(np.ndarray)
def _(series: np.ndarray, state: dict) -> bool:
    return (series.astype(np.int) == series).all()


@integer_contains.register(np.ndarray)
def _(sequence: np.ndarray, state: dict) -> bool:
    return sequence.shape[0] > 0 and np.issubdtype(sequence.dtype, np.integer)

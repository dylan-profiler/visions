import numpy as np

from visions.types.integer import float_is_int, integer_contains, to_int

# https://het.as.utexas.edu/HET/Software/Numpy/reference/arrays.scalars.html


@to_int.register(np.ndarray)
def _(series: np.ndarray, state: dict) -> np.ndarray:
    return series.astype(np.int)


@float_is_int.register(np.ndarray)
def _(series: np.ndarray, state: dict):
    return (series.astype(np.int) == series).all()


@integer_contains.register(np.ndarray)
def _(sequence: np.ndarray, state: dict) -> bool:
    return sequence.shape[0] > 0 and np.issubdtype(sequence.dtype, np.integer)

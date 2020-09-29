import numpy as np

from visions.types.float import Float
from visions.types.integer import Integer


@Integer.register_relationship(Float, np.ndarray)
def float_is_integer(series: np.ndarray, state: dict) -> bool:
    return (series.astype(np.int) == series).all()


@Integer.register_transformer(Float, np.ndarray)
def float_to_integer(series: np.ndarray, state: dict) -> np.ndarray:
    return series.astype(np.int)


@Integer.contains_op.register
def integer_contains(sequence: np.ndarray, state: dict) -> bool:
    return sequence.shape[0] > 0 and np.issubdtype(sequence.dtype, np.integer)

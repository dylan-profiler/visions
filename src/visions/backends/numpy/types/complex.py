import numpy as np

from visions.backends.numpy import test_utils
from visions.backends.numpy.array_utils import array_not_empty
from visions.backends.numpy.types.float import string_is_float
from visions.types.complex import Complex
from visions.types.string import String


def imaginary_in_string(array: np.ndarray, imaginary_indicator: tuple = ("j", "i")):
    return any(any(v in s for v in imaginary_indicator) for s in array)


@Complex.register_relationship(String, np.ndarray)
def string_is_complex(array: np.ndarray, state: dict) -> bool:
    def f(arr: np.array) -> np.array:
        return arr.astype(np.complexfloating)

    coerced_array = test_utils.option_coercion_evaluator(f)(array)
    return (
        coerced_array is not None
        and not string_is_float(array, state)
        and imaginary_in_string(array)
    )


@Complex.register_transformer(String, np.ndarray)
def string_to_complex(array: np.array, state: dict) -> np.ndarray:
    return array.astype(np.complexfloating)


@Complex.contains_op.register
@array_not_empty
def complex_contains(array: np.ndarray, state: dict) -> bool:
    return np.issubdtype(array.dtype, np.complexfloating)

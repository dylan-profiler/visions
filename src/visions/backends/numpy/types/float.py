import numpy as np

from visions.backends.numpy import test_utils
from visions.backends.numpy.array_utils import array_handle_nulls, array_not_empty
from visions.types.complex import Complex
from visions.types.float import Float
from visions.types.string import String
from visions.utils.warning_handling import suppress_warnings


def test_string_leading_zeros(array: np.ndarray, coerced_array: np.ndarray):
    return not any(s[0] == "0" for s in array[coerced_array > 1])


@Float.register_relationship(String, np.ndarray)
@array_handle_nulls
def string_is_float(array: np.ndarray, state: dict) -> bool:
    coerced_array = test_utils.option_coercion_evaluator(
        lambda s: s.astype(np.floating)
    )(array)

    return (
        coerced_array is not None
        and float_contains(coerced_array, state)
        and test_string_leading_zeros(array, coerced_array)
    )


@Float.register_transformer(String, np.ndarray)
def string_to_float(array: np.array, state: dict) -> np.ndarray:
    return array.astype(np.floating)


@Float.register_relationship(Complex, np.ndarray)
def complex_is_float(array: np.array, state: dict) -> bool:
    return all(np.imag(array) == 0)


@Float.register_transformer(Complex, np.ndarray)
def complex_to_float(array: np.array, state: dict) -> np.ndarray:
    return suppress_warnings(lambda s: s.astype(np.floating))(array)


@Float.contains_op.register
@array_handle_nulls
@array_not_empty
def float_contains(array: np.ndarray, state: dict) -> bool:
    return np.issubdtype(array.dtype, np.floating)

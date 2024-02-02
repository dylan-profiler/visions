import numpy as np
from packaging import version

from visions.backends.numpy import test_utils
from visions.backends.numpy.array_utils import array_not_empty
from visions.backends.numpy.types.float import string_is_float
from visions.types.complex import Complex
from visions.types.string import String

_OLD_NUMPY = version.parse(np.version.version) <= version.parse("1.19.0")


def imaginary_in_string(array: np.ndarray, imaginary_indicator: tuple = ("j", "i")):
    return any(any(v in s for v in imaginary_indicator) for s in array)


@Complex.register_transformer(String, np.ndarray)
def string_to_complex(array: np.array, state: dict) -> np.ndarray:
    if _OLD_NUMPY:
        return np.array([complex(v) for v in array])
    else:
        return array.astype(complex)


@Complex.register_relationship(String, np.ndarray)
def string_is_complex(array: np.ndarray, state: dict) -> bool:
    coerced_array = test_utils.option_coercion_evaluator(
        lambda x: string_to_complex(x, state)
    )(array)
    return (
        coerced_array is not None
        and not string_is_float(array, state)
        and imaginary_in_string(array)
    )


@Complex.contains_op.register
@array_not_empty
def complex_contains(array: np.ndarray, state: dict) -> bool:
    return np.issubdtype(array.dtype, complex)

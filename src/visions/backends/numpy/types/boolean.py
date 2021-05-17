from typing import Dict, List

import numpy as np

from visions.backends.numpy.array_utils import (
    array_handle_nulls,
    array_not_empty,
)
from visions.backends.numpy.test_utils import (
    coercion_map,
    coercion_map_test,
)

from visions.backends.python.types.boolean import get_boolean_coercions
from visions.types.boolean import Boolean
from visions.types.object import Object
from visions.types.string import String


string_coercions = get_boolean_coercions("en")


@Boolean.register_relationship(Object, np.ndarray)
@array_handle_nulls
def object_is_boolean(array: np.ndarray, state: dict) -> bool:
    bool_set = {True, False}
    try:
        ret = all(item in bool_set for item in array)
    except (ValueError, TypeError, AttributeError):
        ret = False

    return ret


@Boolean.register_transformer(Object, np.ndarray)
def object_to_boolean(array: np.ndarray, state: dict) -> np.ndarray:
    return array.astype(bool)


@Boolean.register_relationship(String, np.ndarray)
def string_is_boolean(array: np.ndarray, state: dict) -> bool:
    try:
        val_generator = (val.lower() for val in array)
        return coercion_map_test(string_coercions)(val_generator, state)
    except (ValueError, TypeError, AttributeError):
        return False


@Boolean.register_transformer(String, np.ndarray)
def string_to_boolean(array: np.ndarray, state: dict) -> np.ndarray:
    return object_to_boolean(coercion_map(string_coercions)(array.str.lower()), state)


@Boolean.contains_op.register
@array_handle_nulls
@array_not_empty
def boolean_contains(array: np.ndarray, state: dict) -> bool:
    return np.issubdtype(array.dtype, np.bool)

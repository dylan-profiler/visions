from typing import Dict, List

import numpy as np

from visions.backends.numpy.array_utils import (
    array_handle_nulls,
    array_not_empty,
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
def object_to_boolean(array: np.ndarray, state: dict) -> pd.Series:
    return series.astype(bool)


@Boolean.register_relationship(String, np.ndarray)
def string_is_boolean(array: np.ndarray, state: dict) -> bool:
    try:
        val_generator = (val.lower() for val in array)
        return coercion_map_test(string_coercions)(val_generator, state)
    except (ValueError, TypeError, AttributeError):
        return False


@Boolean.register_transformer(String, pd.Series)
def string_to_boolean(series: pd.Series, state: dict) -> pd.Series:
    return object_to_boolean(coercion_map(string_coercions)(series.str.lower()), state)


@Boolean.contains_op.register
@array_handle_nulls
@array_not_empty
def boolean_contains(series: pd.Series, state: dict) -> bool:
    return pdt.is_bool_dtype(series) and not pdt.is_categorical_dtype(series)

from typing import Dict, List

import pandas as pd
import pandas.api.types as pdt

from visions.backends.pandas.series_utils import (
    series_handle_nulls,
    series_not_empty,
    series_not_sparse,
)
from visions.backends.pandas.test_utils import (
    coercion_map,
    coercion_map_test,
    pandas_version,
)
from visions.backends.python.types.boolean import get_boolean_coercions
from visions.types.boolean import Boolean
from visions.types.object import Object
from visions.types.string import String

hasnan_bool_name = "boolean" if pandas_version[0] >= 1 else "Bool"


string_coercions = get_boolean_coercions("en")


@Boolean.register_relationship(Object, pd.Series)
@series_handle_nulls
def object_is_boolean(series: pd.Series, state: dict) -> bool:
    bool_set = {True, False}
    try:
        ret = all(item in bool_set for item in series.values)
    except (ValueError, TypeError, AttributeError):
        ret = False

    return ret


@Boolean.register_transformer(Object, pd.Series)
def object_to_boolean(series: pd.Series, state: dict) -> pd.Series:
    dtype = hasnan_bool_name if series.hasnans else bool
    return series.astype(dtype)


@Boolean.register_relationship(String, pd.Series)
def string_is_boolean(series: pd.Series, state: dict) -> bool:
    try:
        return coercion_map_test(string_coercions)(series.str.lower(), state)
    except (ValueError, TypeError, AttributeError):
        return False


@Boolean.register_transformer(String, pd.Series)
def string_to_boolean(series: pd.Series, state: dict) -> pd.Series:
    return object_to_boolean(coercion_map(string_coercions)(series.str.lower()), state)


@Boolean.contains_op.register
@series_not_sparse
@series_handle_nulls
@series_not_empty
def boolean_contains(series: pd.Series, state: dict) -> bool:
    return pdt.is_bool_dtype(series) and not pdt.is_categorical_dtype(series)

from typing import Dict, List

import pandas as pd
from pandas.api import types as pdt

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
from visions.types.boolean import (
    boolean_contains,
    object_is_bool,
    object_to_bool,
    string_is_bool,
    string_to_bool,
)

hasnan_bool_name = "boolean" if pandas_version[0] >= 1 else "Bool"


def get_boolean_coercions(id: str) -> List[Dict]:
    coercion_map = {
        "default": [{"true": True, "false": False}],
        "en": [
            {"true": True, "false": False},
            {"y": True, "n": False},
            {"yes": True, "no": False},
        ],
        "nl": [
            {"true": True, "false": False},
            {"ja": True, "nee": False},
            {"j": True, "n": False},
        ],
    }
    return coercion_map[id]


string_coercions = get_boolean_coercions("en")


@object_to_bool.register(pd.Series)
def _(series: pd.Series, state: dict) -> pd.Series:
    dtype = hasnan_bool_name if series.hasnans else bool
    return series.astype(dtype)


@object_is_bool.register(pd.Series)
@series_handle_nulls
def _(series: pd.Series, state: dict) -> bool:
    bool_set = {True, False}
    try:
        ret = all(item in bool_set for item in series)
    except:
        ret = False

    return ret


@string_is_bool.register(pd.Series)
def _(series: pd.Series, state: dict) -> bool:
    try:
        return coercion_map_test(string_coercions)(series.str.lower())
    except:
        return False


@string_to_bool.register(pd.Series)
def _(series: pd.Series, state: dict) -> pd.Series:
    return object_to_bool(coercion_map(string_coercions)(series.str.lower()), state)


@boolean_contains.register(pd.Series)
@series_not_sparse
@series_not_empty
def _(series: pd.Series, state: dict) -> bool:
    return pdt.is_bool_dtype(series) and not pdt.is_categorical_dtype(series)

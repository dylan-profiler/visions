from typing import Dict, List

import pandas as pd
from pandas.api import types as pdt

from visions.types.boolean import (
    boolean_contains,
    object_is_bool,
    object_to_bool,
    string_is_bool,
    string_to_bool,
)
from visions.utils.coercion.test_utils import coercion_map, coercion_map_test
from visions.utils.series_utils import (
    func_nullable_series_contains,
    series_not_empty,
    series_not_sparse,
)

hasnan_bool_name = "boolean" if int(pd.__version__.split(".")[0]) >= 1 else "Bool"


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
def _(series: pd.Series, state: dict):
    dtype = hasnan_bool_name if series.hasnans else bool
    return series.astype(dtype)


@object_is_bool.register(pd.Series)
@func_nullable_series_contains
def _(series: pd.Series, state: dict) -> bool:
    bool_set = {True, False}
    try:
        ret = all(item in bool_set for item in series)
    except:
        ret = False

    return ret


@string_is_bool.register(pd.Series)
def _(series: pd.Series, state: dict):
    try:
        return coercion_map_test(string_coercions)(series.str.lower())
    except:
        return False


@string_to_bool.register(pd.Series)
def _(series, state: dict):
    try:
        return object_to_bool(coercion_map(string_coercions)(series.str.lower()), state)
    except:
        return False


@series_not_sparse
@series_not_empty
def tmp_op(cls, series, state):
    if not pdt.is_categorical_dtype(series) and pdt.is_bool_dtype(series):
        return True

    return False


@boolean_contains.register(pd.Series)
def _(series: pd.Series, state: dict):
    return tmp_op(_, series, state)

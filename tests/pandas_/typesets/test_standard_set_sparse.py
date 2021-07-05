from typing import Dict, Set, Type, cast

import pytest

from visions import StandardSet, VisionsBaseType
from visions.backends.pandas.test_utils import pandas_version
from visions.test.series_sparse import get_sparse_series
from visions.test.utils import contains, get_contains_cases, get_inference_cases, infers
from visions.types import (
    Boolean,
    Categorical,
    Complex,
    DateTime,
    Float,
    Generic,
    Integer,
    Object,
    String,
    TimeDelta,
)

not_pandas_1_0_5 = not (
    (pandas_version[0] == 1) and (pandas_version[1] == 0) and (pandas_version[2] == 5)
)

series = get_sparse_series()

typeset = StandardSet()

contains_map: Dict[Type[VisionsBaseType], Set[str]] = {
    DateTime: set(),
    TimeDelta: set(),
    Categorical: set(),
    Object: set(),
    Integer: set(),
    Complex: set(),
    Float: set(),
    Boolean: set(),
    String: set(),
    Generic: {
        "int_sparse",
        "pd_int64_sparse",
        "float_sparse",
        "bool_sparse",
        "complex_sparse",
        "str_obj_sparse",
    },
}


if pandas_version[0] >= 1 and not_pandas_1_0_5:
    contains_map[Generic].add("pd_bool_sparse")
    contains_map[Generic].add("pd_string_sparse")


@pytest.mark.parametrize(**get_contains_cases(series, contains_map, typeset))
def test_contains(name, series, contains_type, member):
    """Test the generated combinations for "series in type"

    Args:
        series: the series to test
        contains_type: the type to test against
        member: the result
    """
    result, message = contains(name, series, contains_type, member)
    assert result, message


inference_map: Dict[str, Type[VisionsBaseType]] = {
    "int_sparse": Generic,
    "pd_int64_sparse": Generic,
    "float_sparse": Generic,
    "bool_sparse": Generic,
    "pd_bool_sparse": Generic,
    "complex_sparse": Generic,
    "str_obj_sparse": Generic,
    "pd_categorical_sparse": Generic,
    # "datetime_sparse": Generic,
}

if pandas_version[0] >= 1 and not_pandas_1_0_5:
    inference_map["pd_bool_sparse"] = Generic
    inference_map["pd_string_sparse"] = Generic


@pytest.mark.parametrize(**get_inference_cases(series, inference_map, typeset))
def test_inference(name, series, inference_type, typeset, difference):
    """Test the generated combinations for "inference(series) == type"

    Args:
        series: the series to test
        inference_type: the type to test against
    """
    result, message = infers(name, series, inference_type, typeset, difference)
    assert result, message


@pytest.mark.parametrize("series", series)
def test_detect_type(series):
    typeset.detect_type(series)


@pytest.mark.parametrize("series", series)
def test_cast_inferred(series):
    typeset.cast_to_inferred(series)

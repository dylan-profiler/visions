import pandas as pd
import pytest

from visions import StandardSet
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

series = get_sparse_series()

typeset = StandardSet()

contains_map = {
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

if int(pd.__version__.split(".")[0]) >= 1:
    contains_map[Generic].add("pd_bool_sparse")
    contains_map[Generic].add("pd_string_sparse")


@pytest.mark.parametrize(**get_contains_cases(series, contains_map, typeset))
def test_contains(series, type, member):
    """Test the generated combinations for "series in type"

    Args:
        series: the series to test
        type: the type to test against
        member: the result
    """
    result, message = contains(series, type, member)
    assert result, message


inference_map = {
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

if int(pd.__version__.split(".")[0]) >= 1:
    inference_map["pd_bool_sparse"] = Generic
    inference_map["pd_string_sparse"] = Generic


@pytest.mark.parametrize(**get_inference_cases(series, inference_map, typeset))
def test_inference(series, type, typeset, difference):
    """Test the generated combinations for "inference(series) == type"

    Args:
        series: the series to test
        type: the type to test against
    """
    result, message = infers(series, type, typeset, difference)
    assert result, message


@pytest.mark.parametrize("series", series)
def test_detect_type(series):
    typeset.detect_type(series)


@pytest.mark.parametrize("series", series)
def test_cast_inferred(series):
    typeset.cast_to_inferred(series)

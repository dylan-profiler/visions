import pytest

from tests.series_sparse import get_sparse_series
from tests.utils import (
    contains,
    get_contains_cases,
    get_inference_cases,
    infers,
)
from visions import StandardSet
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
    Generic: set(),
    # DateTime: {"datetime_sparse"},
    DateTime: set(),
    TimeDelta: set(),
    Categorical: set(),
    Object: set(),
    Integer: {"int_sparse", "pd_int64_sparse"},
    Float: {"float_sparse"},
    Boolean: {"bool_sparse", "pd_bool_sparse"},
    Complex: {"complex_sparse"},
    String: {"str_obj_sparse"},
}


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
    "int_sparse": Integer,
    "pd_int64_sparse": Integer,
    "float_sparse": Float,
    "bool_sparse": Boolean,
    "pd_bool_sparse": Boolean,
    "complex_sparse": Complex,
    "str_obj_sparse": String,
    # "datetime_sparse": DateTime,
}


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

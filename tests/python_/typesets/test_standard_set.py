from typing import Dict, Set, Type

import pytest

from visions import StandardSet, VisionsBaseType
from visions.backends.python.sequences import get_sequences
from visions.test.utils import (
    cast,
    contains,
    convert,
    get_cast_cases,
    get_contains_cases,
    get_convert_cases,
    get_inference_cases,
    infers,
)
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

sequences = get_sequences()

typeset = StandardSet()

contains_map: Dict[Type[VisionsBaseType], Set[str]] = {
    Integer: {
        "int_series",
        "int_range",
        "int_series_boolean",
    },
    Float: {
        "float_series",
        "float_series2",
    },
    Categorical: set(),
    Boolean: {"bool_series", "bool_nan_series"},
    Complex: {
        "complex_series_py",
        "complex_series_py_float",
    },
    DateTime: set(),
    TimeDelta: set(),
    String: {
        "py_datetime_str",
        "timestamp_string_series",
        "string_series",
        "string_unicode_series",
        "path_series_linux_str",
        "path_series_windows_str",
        "string_date",
        "textual_float",
        "textual_float_nan",
        "ip_str",
        "string_flt",
        "string_num",
        "str_url",
        "string_bool_nan",
        "str_complex",
        "str_complex_nan",
        "uuid_series_str",
        "str_int_leading_zeros",
        "email_address_str",
        "str_float_non_leading_zeros",
        "str_int_zeros",
    },
    Object: {
        "path_series_linux",
        "path_series_linux_missing",
        "path_series_windows",
        "url_series",
        "url_none_series",
        "file_test_py",
        "file_mixed_ext",
        "file_test_py_missing",
        "image_png",
        "image_png_missing",
        "image_png",
        "image_png_missing",
        "email_address",
        "email_address_missing",
        "uuid_series",
        "uuid_series_missing",
        "ip",
        "ip_mixed_v4andv6",
        "ip_missing",
        "mixed_list[str,int]",
        "mixed_dict",
        "callable",
        "module",
        "mixed_integer",
        "mixed_list",
        "date",
        "time",
    },
    Generic: {
        "empty",
    },
}


@pytest.mark.parametrize(**get_contains_cases(sequences, contains_map, typeset))
def test_contains(name, series, type, member):
    """Test the generated combinations for "series in type"

    Args:
        series: the series to test
        type: the type to test against
        member: the result
    """
    result, message = contains(name, series, type, member)
    assert result, message


inference_map = {
    "int_series": Integer,
    "int_range": Integer,
    "float_series": Float,
    "int_series_boolean": Integer,
    "float_series2": Integer,
    "complex_series_float": Integer,
    "string_series": String,
    "categorical_string_series": Categorical,
    "timestamp_string_series": String,
    "string_unicode_series": String,
    "string_num": Integer,
    "complex_series_py_float": Integer,
    "string_flt": Float,
    "string_bool_nan": Boolean,
    "string_date": String,
    "py_datetime_str": DateTime,
    "str_url": String,
    "bool_series": Boolean,
    "bool_nan_series": Boolean,
    "complex_series_py": Complex,
    "geometry_series_missing": Object,
    "geometry_series": Object,
    "path_series_linux": Object,
    "path_series_linux_missing": Object,
    "path_series_linux_str": String,
    "path_series_windows": Object,
    "path_series_windows_str": String,
    "url_series": Object,
    "url_none_series": Object,
    "mixed_list[str,int]": Object,
    "mixed_dict": Object,
    "mixed_integer": Object,
    "mixed_list": Object,
    "callable": Object,
    "module": Object,
    "textual_float": Float,
    "textual_float_nan": Float,
    "empty": Generic,
    "empty_object": Generic,
    "empty_float": Generic,
    "ip": Object,
    "ip_str": String,
    "ip_missing": Object,
    "date": Object,
    "time": Object,
    "str_complex": Complex,
    "str_complex_nan": Complex,
    "uuid_series": Object,
    "uuid_series_str": String,
    "uuid_series_missing": Object,
    "ip_mixed_v4andv6": Object,
    "file_test_py": Object,
    "file_test_py_missing": Object,
    "file_mixed_ext": Object,
    "image_png": Object,
    "image_png_missing": Object,
    "str_int_leading_zeros": String,
    "str_float_non_leading_zeros": Float,
    "str_int_zeros": Integer,
    "email_address": Object,
    "email_address_missing": Object,
    "email_address_str": String,
}


@pytest.mark.parametrize(**get_inference_cases(sequences, inference_map, typeset))
def test_inference(name, series, type, typeset, difference):
    """Test the generated combinations for "inference(series) == type"

    Args:
        series: the series to test
        type: the type to test against
    """
    result, message = infers(name, series, type, typeset, difference)
    assert result, message


# Conversions in one single step
convert_map = [
    # Model type, Relation type
    (Integer, Float, {"float_series2"}),
    (
        Complex,
        String,
        {
            "str_complex",
            "str_complex_nan",
            "textual_float_nan",
            "str_int_zeros",
            "textual_float",
            "string_num",
            "string_flt",
            "str_float_non_leading_zeros",
        },
    ),
    (
        Float,
        String,
        {
            "string_flt",
            "string_num",
            "textual_float",
            "textual_float_nan",
            "str_float_non_leading_zeros",
            "str_int_zeros",
        },
    ),
    (Boolean, String, {"string_bool_nan"}),
    (Boolean, Object, {"bool_nan_series"}),
    (Float, Complex, {"complex_series_py_float"}),
    (DateTime, String, {"py_datetime_str"}),
]


@pytest.mark.parametrize(**get_convert_cases(sequences, convert_map, typeset))
def test_conversion(name, source_type, relation_type, series, member):
    """Test the generated combinations for "convert(series) == type" and "infer(series) = source_type"

    Args:
        series: the series to test
        type: the type to test against
    """
    result, message = convert(name, source_type, relation_type, series, member)
    assert result, message


#
# cast_results = {
#     "float_series2": [1, 2, 3, 4],
#     "string_num": pd.Series([1, 2, 3], dtype=np.int64),
#     "string_flt": pd.Series([1.0, 45.67, 3.5], dtype=np.float64),
#     "string_bool_nan": pd.Series([True, False, None], dtype=hasnan_bool_name),
#     "str_float_non_leading_zeros": pd.Series([0.0, 0.04, 0.0], dtype=np.float64),
#     "str_int_zeros": pd.Series([0, 0, 0, 2], dtype=np.int64),
#     "bool_nan_series": pd.Series([True, False, None], dtype=hasnan_bool_name),
#     "str_complex": pd.Series(
#         [complex(1, 1), complex(2, 2), complex(10, 100)], dtype=np.complex128
#     ),
#     "str_complex_nan": pd.Series(
#         [complex(1, 1), complex(2, 2), complex(10, 100), np.nan], dtype=np.complex128
#     ),
#     "textual_float": pd.Series([1.1, 2.0], dtype=np.float64),
#     "textual_float_nan": pd.Series([1.1, 2.0, np.nan], dtype=np.float64),
#     "mixed": pd.Series([True, False, None], dtype=hasnan_bool_name),
# }
#
#
# @pytest.mark.parametrize(**get_cast_cases(series, cast_results))
# def test_cast(series, expected):
#     if isinstance(expected, str):
#         expected = None
#     result, message = cast(series, typeset, expected)
#     assert result, message

import numpy as np
import pandas as pd
import pytest

from visions.test.series import get_series
from visions.test.series_geometry import get_geometry_series
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
from visions.typesets.standard_set import StandardSet


def reload_series_to_numpy(s):
    return np.array(s.tolist())


array = get_series()
array.update(get_geometry_series())
array = {k: v.to_numpy() for k, v in array.items()}

# Pandas doesn't correctly handle complex categoricals pending
# https://github.com/pandas-dev/pandas/pull/36482/
array.pop("categorical_complex_series")

# Some sequences don't round trip correctly from pandas (i.e. Series.to_numpy()
# is not equivalent to np.array(Series.tolist())
array["Int64_int_series"] = reload_series_to_numpy(array["Int64_int_series"])
array["pd_uint32"] = reload_series_to_numpy(array["pd_uint32"])

typeset = StandardSet() - Categorical

contains_map = {
    Integer: {
        "int_series",
        "Int64_int_series",
        "int_range",
        "Int64_int_nan_series",
        "int_series_boolean",
        "np_uint32",
        "pd_uint32",
        "categorical_int_series",
    },
    Float: {
        "float_series",
        "float_series2",
        "float_series3",
        "float_series4",
        "inf_series",
        "float_nan_series",
        "float_series5",
        "int_nan_series",
        "float_with_inf",
        "float_series6",
        "categorical_float_series",
    },
    Boolean: {
        "bool_series",
        "bool_series2",
        "bool_series3",
        "nullable_bool_series",
        "bool_nan_series",
        "mixed",
    },
    Complex: {
        "complex_series",
        "complex_series_py",
        "complex_series_nan",
        "complex_series_py_nan",
        "complex_series_nan_2",
        "complex_series_float",
        "complex_series_py_float",
        # "categorical_complex_series",
    },
    DateTime: {
        "timestamp_series",
        "timestamp_aware_series",
        "datetime",
        "timestamp_series_nat",
        "date_series_nat",
    },
    TimeDelta: {"timedelta_series", "timedelta_series_nat", "timedelta_negative"},
    String: {
        "py_datetime_str",
        "timestamp_string_series",
        "string_with_sep_num_nan",
        "string_series",
        "geometry_string_series",
        "string_unicode_series",
        "string_np_unicode_series",
        "path_series_linux_str",
        "path_series_windows_str",
        "int_str_range",
        "string_date",
        "textual_float",
        "textual_float_nan",
        "ip_str",
        "string_flt",
        "string_num",
        "str_url",
        "string_str_nan",
        "string_num_nan",
        "string_bool_nan",
        "string_flt_nan",
        "str_complex",
        "str_complex_nan",
        "uuid_series_str",
        "str_int_leading_zeros",
        "email_address_str",
        "str_float_non_leading_zeros",
        "str_int_zeros",
        "all_null_empty_str",
        "categorical_string_series",
        "categorical_char",
        "string_dtype_series",
        "ordinal",
    },
}


contains_map[Object] = {
    "path_series_linux",
    "path_series_linux_missing",
    "path_series_windows",
    "url_series",
    "url_nan_series",
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
    "geometry_series",
    "geometry_series_missing",
    "mixed_list[str,int]",
    "mixed_dict",
    "callable",
    "module",
    "mixed_integer",
    "mixed_list",
    "date",
    "time",
    "ordinal",
}

# Empty series
contains_map[Generic] = {
    "empty",
    "empty_bool",
    "empty_float",
    "empty_int64",
    "empty_object",
    "all_null_none",
    "all_null_nan",
    "all_null_nat",
    "nan_series",
    "nan_series_2",
}


@pytest.mark.parametrize(**get_contains_cases(array, contains_map, typeset))
def test_contains(name, series, contains_type, member):
    """Test the generated combinations for "array in type"

    Args:
        series: the series to test
        contains_type: the type to test against
        member: the result
    """
    result, message = contains(name, series, contains_type, member)
    assert result, message


inference_map = {
    "int_series": Integer,
    "categorical_int_series": Integer,
    "int_nan_series": Integer,
    "Int64_int_series": Integer,
    "Int64_int_nan_series": Integer,
    "np_uint32": Integer,
    "pd_uint32": Integer,
    "int_range": Integer,
    "float_series": Float,
    "float_nan_series": Float,
    "int_series_boolean": Integer,
    "complex_series_py_float": Integer,
    "float_series2": Integer,
    "float_series3": Float,
    "float_series4": Float,
    "float_series5": Float,
    "float_series6": Float,
    "complex_series_float": Integer,
    "categorical_float_series": Float,
    "float_with_inf": Float,
    "inf_series": Float,
    "nan_series": Generic,
    "nan_series_2": Generic,
    "py_datetime_str": DateTime,
    "string_series": String,
    "categorical_string_series": String,
    "timestamp_string_series": DateTime,
    "string_with_sep_num_nan": String,  # TODO: Introduce thousands separator
    "string_unicode_series": String,
    "string_np_unicode_series": String,
    "string_num_nan": Integer,
    "string_num": Integer,
    "string_flt_nan": Float,
    "string_flt": Float,
    "string_str_nan": String,
    "string_bool_nan": Boolean,
    "int_str_range": Integer,
    "string_date": DateTime,
    "str_url": String,
    "bool_series": Boolean,
    "bool_nan_series": Boolean,
    "nullable_bool_series": Boolean,
    "bool_series2": Boolean,
    "bool_series3": Boolean,
    "complex_series": Complex,
    "complex_series_nan": Complex,
    "complex_series_nan_2": Complex,
    "complex_series_py_nan": Complex,
    "complex_series_py": Complex,
    # "categorical_complex_series": Complex,
    "timestamp_series": DateTime,
    "timestamp_series_nat": DateTime,
    "timestamp_aware_series": DateTime,
    "datetime": DateTime,
    "timedelta_series": TimeDelta,
    "timedelta_series_nat": TimeDelta,
    "timedelta_negative": TimeDelta,
    "geometry_string_series": String,
    "geometry_series_missing": Object,
    "geometry_series": Object,
    "path_series_linux": Object,
    "path_series_linux_missing": Object,
    "path_series_linux_str": String,
    "path_series_windows": Object,
    "path_series_windows_str": String,
    "url_series": Object,
    "url_nan_series": Object,
    "url_none_series": Object,
    "mixed_list[str,int]": Object,
    "mixed_dict": Object,
    "mixed_integer": Object,
    "mixed_list": Object,
    "mixed": Boolean,
    "callable": Object,
    "module": Object,
    "textual_float": Float,
    "textual_float_nan": Float,
    "empty": Generic,
    "empty_object": Generic,
    "empty_float": Generic,
    "empty_bool": Generic,
    "empty_int64": Generic,
    "ip": Object,
    "ip_str": String,
    "ip_missing": Object,
    "date_series_nat": DateTime,
    "date": Object,
    "time": Object,
    "categorical_char": String,
    "ordinal": String,
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
    "all_null_none": Generic,
    "all_null_nan": Generic,
    "all_null_nat": Generic,
    "all_null_empty_str": String,
    "string_dtype_series": String,
}


@pytest.mark.parametrize(**get_inference_cases(array, inference_map, typeset))
def test_inference(name, series, inference_type, typeset, difference):
    """Test the generated combinations for "inference(array) == type"

    Args:
        series: the array to test
        inference_type: the type to test against
    """
    result, message = infers(name, series, inference_type, typeset, difference)
    assert result, message


# Conversions in one single step
convert_map = [
    # Model type, Relation type
    (Integer, Float, {"int_nan_series", "float_series2"}),
    (Complex, String, {"str_complex", "str_complex_nan"}),
    (
        Float,
        String,
        {
            "string_flt",
            "string_num_nan",
            "string_num",
            "string_flt_nan",
            "textual_float",
            "textual_float_nan",
            "int_str_range",
            "str_float_non_leading_zeros",
            "str_int_zeros",
            # "string_with_sep_num_nan",
        },
    ),
    (DateTime, String, {"timestamp_string_series", "string_date", "py_datetime_str"}),
    (Boolean, String, {"string_bool_nan"}),
    (Float, Complex, {"complex_series_float", "complex_series_py_float"}),
    (Boolean, Object, {"bool_nan_series", "mixed", "nullable_bool_series"}),
]


@pytest.mark.parametrize(**get_convert_cases(array, convert_map, typeset))
def test_conversion(name, source_type, relation_type, series, member):
    """Test the generated combinations for "convert(array) == type" and "infer(array) = source_type"

    Args:
        series: the array to test
        type: the type to test against
    """
    result, message = convert(name, source_type, relation_type, series, member)
    assert result, message


cast_results = {
    "float_series2": pd.Series([1, 2, 3, 4], dtype=np.int64),
    "int_nan_series": pd.Series([1, 2, np.nan], dtype=pd.Int64Dtype()),
    "timestamp_string_series": pd.Series(
        [np.datetime64("1941-05-24"), np.datetime64("2016-10-13")],
        dtype="datetime64[ns]",
    ),
    "py_datetime_str": pd.Series(
        [np.datetime64("1941-05-24 00:05:00"), np.datetime64("2016-10-13 00:10:00")],
        dtype="datetime64[ns]",
    ),
    "string_num_nan": pd.Series([1, 2, np.nan], dtype=pd.Int64Dtype()),
    "string_num": pd.Series([1, 2, 3], dtype=np.int64),
    "string_flt_nan": pd.Series([1.0, 45.67, np.nan], dtype=np.float64),
    "string_flt": pd.Series([1.0, 45.67, 3.5], dtype=np.float64),
    "string_bool_nan": np.array([True, False, None]),
    "int_str_range": pd.Series(
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
        dtype=np.int64,
    ),
    "string_date": pd.Series(
        [np.datetime64("1937-05-06"), np.datetime64("2014-04-20")],
        dtype="datetime64[ns]",
    ),
    "str_float_non_leading_zeros": pd.Series([0.0, 0.04, 0.0], dtype=np.float64),
    "str_int_zeros": pd.Series([0, 0, 0, 2], dtype=np.int64),
    "bool_nan_series": np.array([True, False, None]),
    "str_complex": pd.Series(
        [complex(1, 1), complex(2, 2), complex(10, 100)], dtype=np.complex128
    ),
    "str_complex_nan": pd.Series(
        [complex(1, 1), complex(2, 2), complex(10, 100), np.nan], dtype=np.complex128
    ),
    "complex_series_float": pd.Series([0, 1, 3, -1], dtype=np.int64),
    "complex_series_py_float": pd.Series([0, 1, 3], dtype=np.int64),
    "textual_float": pd.Series([1.1, 2.0], dtype=np.float64),
    "textual_float_nan": pd.Series([1.1, 2.0, np.nan], dtype=np.float64),
    "mixed": np.array([True, False, np.nan]),
}
cast_results = {
    k: v.to_numpy() if isinstance(v, pd.Series) else v for k, v in cast_results.items()
}


@pytest.mark.parametrize(**get_cast_cases(array, cast_results))
def test_cast(name, series, expected):
    if isinstance(expected, str):
        expected = None
    result, message = cast(name, series, typeset, expected)
    assert result, message

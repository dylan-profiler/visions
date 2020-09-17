import pandas as pd
import pytest

from visions import CompleteSet
from visions.test.series import get_geometry_series, get_series
from visions.test.utils import (
    contains,
    convert,
    get_contains_cases,
    get_convert_cases,
    get_inference_cases,
    infers,
)
from visions.types import (
    URL,
    UUID,
    Boolean,
    Categorical,
    Complex,
    Count,
    Date,
    DateTime,
    EmailAddress,
    File,
    Float,
    Generic,
    Geometry,
    Image,
    Integer,
    IPAddress,
    Object,
    Ordinal,
    Path,
    String,
    Time,
    TimeDelta,
)

series = get_series() + get_geometry_series()

typeset = CompleteSet()

contains_map = {
    Integer: {
        "int_series",
        "Int64_int_series",
        "int_range",
        "Int64_int_nan_series",
        "int_series_boolean",
    },
    Count: {"np_uint32", "pd_uint32"},
    Path: {"path_series_linux", "path_series_linux_missing", "path_series_windows"},
    URL: {"url_series", "url_nan_series", "url_none_series"},
    Float: {
        "float_series",
        "float_series2",
        "float_series3",
        "float_series4",
        "inf_series",
        "nan_series",
        "float_nan_series",
        "float_series5",
        "int_nan_series",
        "nan_series_2",
        "float_with_inf",
        "float_series6",
    },
    Categorical: {
        "categorical_int_series",
        "categorical_float_series",
        "categorical_string_series",
        "categorical_complex_series",
        "categorical_char",
        "ordinal",
    },
    Boolean: {"bool_series", "bool_series2", "bool_series3", "nullable_bool_series"},
    Complex: {
        "complex_series",
        "complex_series_py",
        "complex_series_nan",
        "complex_series_py_nan",
        "complex_series_nan_2",
        "complex_series_float",
    },
    DateTime: {
        "timestamp_series",
        "timestamp_aware_series",
        "datetime",
        "timestamp_series_nat",
        "date_series_nat",
    },
    Date: {"date"},
    Time: {"time"},
    TimeDelta: {"timedelta_series", "timedelta_series_nat", "timedelta_negative"},
    String: {
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
    },
    Geometry: {"geometry_series", "geometry_series_missing"},
    IPAddress: {"ip", "ip_mixed_v4andv6", "ip_missing"},
    Ordinal: {"ordinal"},
    UUID: {"uuid_series", "uuid_series_missing"},
    File: {
        "file_test_py",
        "file_mixed_ext",
        "file_test_py_missing",
        "image_png",
        "image_png_missing",
    },
    Image: {"image_png", "image_png_missing"},
    EmailAddress: {"email_address", "email_address_missing"},
}

if int(pd.__version__[0]) >= 1:
    contains_map[String].add("string_dtype_series")

contains_map[Object] = {
    "mixed_list[str,int]",
    "mixed_dict",
    "callable",
    "module",
    "mixed_integer",
    "mixed_list",
    "mixed",
    "bool_nan_series",
}

# Empty series
contains_map[Generic] = {
    "empty",
    "empty_bool",
    "empty_float",
    "empty_int64",
    "empty_object",
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
    "int_series": Integer,
    "categorical_int_series": Categorical,
    "int_nan_series": Integer,
    "Int64_int_series": Integer,
    "Int64_int_nan_series": Integer,
    "np_uint32": Count,
    "pd_uint32": Count,
    "int_range": Integer,
    "float_series": Float,
    "float_nan_series": Float,
    "int_series_boolean": Integer,
    "float_series2": Integer,
    "float_series3": Float,
    "float_series4": Float,
    "float_series5": Float,
    "float_series6": Float,
    "complex_series_float": Integer,
    "categorical_float_series": Categorical,
    "float_with_inf": Float,
    "inf_series": Float,
    "nan_series": Float,
    "nan_series_2": Float,
    "string_series": String,
    "categorical_string_series": Categorical,
    "timestamp_string_series": Date,
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
    "string_date": Date,
    "str_url": URL,
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
    "categorical_complex_series": Categorical,
    "timestamp_series": DateTime,
    "timestamp_series_nat": DateTime,
    "timestamp_aware_series": DateTime,
    "datetime": Date,
    "timedelta_series": TimeDelta,
    "timedelta_series_nat": TimeDelta,
    "timedelta_negative": TimeDelta,
    "geometry_string_series": Geometry,
    "geometry_series_missing": Geometry,
    "geometry_series": Geometry,
    "path_series_linux": Path,
    "path_series_linux_missing": Path,
    "path_series_linux_str": Path,
    "path_series_windows": Path,
    "path_series_windows_str": Path,
    "url_series": URL,
    "url_nan_series": URL,
    "url_none_series": URL,
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
    "ip": IPAddress,
    "ip_str": IPAddress,
    "ip_missing": IPAddress,
    "date_series_nat": Date,
    "date": Date,
    "time": Time,
    "categorical_char": Categorical,
    "ordinal": Ordinal,
    "str_complex": Complex,
    "str_complex_nan": Complex,
    "uuid_series": UUID,
    "uuid_series_str": UUID,
    "uuid_series_missing": UUID,
    "ip_mixed_v4andv6": IPAddress,
    "file_test_py": File,
    "file_test_py_missing": File,
    "file_mixed_ext": File,
    "image_png": Image,
    "image_png_missing": Image,
    "str_int_leading_zeros": String,
    "str_float_non_leading_zeros": Float,
    "str_int_zeros": Integer,
    "email_address": EmailAddress,
    "email_address_missing": EmailAddress,
    "email_address_str": EmailAddress,
}
if int(pd.__version__[0]) >= 1:
    inference_map["string_dtype_series"] = String


@pytest.mark.parametrize(**get_inference_cases(series, inference_map, typeset))
def test_inference(series, type, typeset, difference):
    """Test the generated combinations for "inference(series) == type"

    Args:
        series: the series to test
        type: the type to test against
    """
    result, message = infers(series, type, typeset, difference)
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
    (Date, DateTime, {"date_series_nat", "datetime"}),
    (DateTime, String, {"timestamp_string_series", "string_date"}),
    (Geometry, String, {"geometry_string_series"}),
    (Boolean, String, {"string_bool_nan"}),
    (IPAddress, String, {"ip_str"}),
    (URL, String, {"str_url"}),
    (Path, String, {"path_series_windows_str", "path_series_linux_str"}),
    (EmailAddress, String, {"email_address_str"}),
    (Float, Complex, {"complex_series_float"}),
    (Boolean, Object, {"bool_nan_series", "mixed"}),
    (UUID, String, {"uuid_series_str"}),
]


@pytest.mark.parametrize(**get_convert_cases(series, convert_map, typeset))
def test_conversion(source_type, relation_type, series, member):
    """Test the generated combinations for "convert(series) == type" and "infer(series) = source_type"

    Args:
        series: the series to test
        type: the type to test against
    """
    result, message = convert(source_type, relation_type, series, member)
    assert result, message


# TODO: cast...

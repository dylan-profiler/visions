import datetime
import uuid
from ipaddress import IPv4Address
from pathlib import PurePosixPath, PureWindowsPath
from urllib.parse import urlparse

import numpy as np
import pandas as pd
import pytest
from shapely import wkt

from visions import CompleteSet
from visions.backends.pandas.test_utils import pandas_version
from visions.backends.pandas.types.boolean import hasnan_bool_name
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
from visions.types.email_address import FQDA

series = get_series()
series.update(get_geometry_series())

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
        "float_nan_series",
        "float_series5",
        "int_nan_series",
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
        "complex_series_py_float",
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

if pandas_version[0] >= 1:
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
    "all_null_nan",
    "all_null_nat",
    "all_null_none",
    "nan_series",
    "nan_series_2",
}


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
    "nan_series": Generic,
    "nan_series_2": Generic,
    "string_series": String,
    "categorical_string_series": Categorical,
    "timestamp_string_series": Date,
    "string_with_sep_num_nan": String,  # TODO: Introduce thousands separator
    "string_unicode_series": String,
    "string_np_unicode_series": String,
    "complex_series_py_float": Integer,
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
    "py_datetime_str": DateTime,
    "all_null_nan": Generic,
    "all_null_nat": Generic,
    "all_null_none": Generic,
    "all_null_empty_str": String,
}
if pandas_version[0] >= 1:
    inference_map["string_dtype_series"] = String


@pytest.mark.parametrize(**get_inference_cases(series, inference_map, typeset))
def test_inference(name, series, inference_type, typeset, difference):
    """Test the generated combinations for "inference(series) == type"

    Args:
        series: the series to test
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
    (Date, DateTime, {"date_series_nat", "datetime"}),
    (DateTime, String, {"timestamp_string_series", "string_date", "py_datetime_str"}),
    (Geometry, String, {"geometry_string_series"}),
    (Boolean, String, {"string_bool_nan"}),
    (IPAddress, String, {"ip_str"}),
    (URL, String, {"str_url"}),
    (Path, String, {"path_series_windows_str", "path_series_linux_str"}),
    (EmailAddress, String, {"email_address_str"}),
    (Float, Complex, {"complex_series_float", "complex_series_py_float"}),
    (Boolean, Object, {"bool_nan_series", "mixed"}),
    (UUID, String, {"uuid_series_str"}),
]


@pytest.mark.parametrize(**get_convert_cases(series, convert_map, typeset))
def test_conversion(name, source_type, relation_type, series, member):
    """Test the generated combinations for "convert(series) == type" and "infer(series) = source_type"

    Args:
        series: the series to test
        type: the type to test against
    """
    result, message = convert(name, source_type, relation_type, series, member)
    assert result, message


cast_results = {
    "float_series2": pd.Series([1, 2, 3, 4], dtype=np.int64),
    "int_nan_series": pd.Series([1, 2, np.nan], dtype=pd.Int64Dtype()),
    "string_num_nan": pd.Series([1, 2, np.nan], dtype=pd.Int64Dtype()),
    "string_num": pd.Series([1, 2, 3], dtype=np.int64),
    "string_flt_nan": pd.Series([1.0, 45.67, np.nan], dtype=np.float64),
    "string_flt": pd.Series([1.0, 45.67, 3.5], dtype=np.float64),
    "string_bool_nan": pd.Series([True, False, None], dtype=hasnan_bool_name),
    "int_str_range": pd.Series(
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
        dtype=np.int64,
    ),
    "str_float_non_leading_zeros": pd.Series([0.0, 0.04, 0.0], dtype=np.float64),
    "str_int_zeros": pd.Series([0, 0, 0, 2], dtype=np.int64),
    "bool_nan_series": pd.Series([True, False, None], dtype=hasnan_bool_name),
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
    "mixed": pd.Series([True, False, None], dtype=hasnan_bool_name),
    "uuid_series_str": pd.Series(
        [
            uuid.UUID("0b8a22ca-80ad-4df5-85ac-fa49c44b7ede"),
            uuid.UUID("aaa381d6-8442-4f63-88c8-7c900e9a23c6"),
            uuid.UUID("00000000-0000-0000-0000-000000000000"),
        ],
    ),
    "ip_str": pd.Series(
        [IPv4Address("127.0.0.1"), IPv4Address("127.0.0.1")],
    ),
    "geometry_string_series": pd.Series(
        [
            wkt.loads("POINT (-92 42)"),
            wkt.loads("POINT (-92 42.1)"),
            wkt.loads("POINT (-92 42.2)"),
        ],
    ),
    "email_address_str": pd.Series(
        [FQDA("test", "example.com"), FQDA("info", "example.eu")],
    ),
    "str_url": pd.Series(
        [
            urlparse("http://www.cwi.nl:80/%7Eguido/Python.html"),
            urlparse("https://github.com/dylan-profiling/hurricane"),
        ],
    ),
    "path_series_windows_str": pd.Series(
        [
            PureWindowsPath("C:\\home\\user\\file.txt"),
            PureWindowsPath("C:\\home\\user\\test2.txt"),
        ],
    ),
    "path_series_linux_str": pd.Series(
        [PurePosixPath("/home/user/file.txt"), PurePosixPath("/home/user/test2.txt")],
    ),
    "datetime": pd.Series(
        [
            datetime.date(2011, 1, 1),
            datetime.date(2012, 1, 2),
            datetime.date(2013, 1, 1),
        ],
    ),
    "date_series_nat": pd.Series(
        [datetime.date(2017, 3, 5), datetime.date(2019, 12, 4), pd.NaT],
    ),
    "timestamp_string_series": pd.Series(
        [datetime.date(1941, 5, 24), datetime.date(2016, 10, 13)]
    ),
    "py_datetime_str": pd.Series(
        [datetime.date(1941, 5, 24), datetime.date(2016, 10, 13)]
    ),
    "string_date": pd.Series([datetime.date(1937, 5, 6), datetime.date(2014, 4, 20)]),
}


@pytest.mark.parametrize(**get_cast_cases(series, cast_results))
def test_cast(name, series, expected):
    if isinstance(expected, str):
        expected = None
    result, message = cast(name, series, typeset, expected)
    assert result, message

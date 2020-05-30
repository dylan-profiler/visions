import pytest

from visions import Generic
from visions.types.measurement_level import Nominal, Interval, Ratio, Ordinal

from tests.utils import get_contains_cases, contains


def get_contains_map():
    series_map = {
        Interval: [
            "int_series",
            "Int64_int_series",
            "int_range",
            "Int64_int_nan_series",
            "int_series_boolean",
            "np_unint32",
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
            "complex_series",
            "complex_series_py",
            "complex_series_nan",
            "complex_series_py_nan",
            "complex_series_nan_2",
            "complex_series_float",
            "timestamp_series",
            "timestamp_aware_series",
            "datetime",
            "timestamp_series_nat",
            "date_series_nat",
            "date",
            "time",
        ],
        Nominal: [
            "path_series_linux",
            "path_series_linux_missing",
            "path_series_windows",
            "url_series",
            "url_nan_series",
            "url_none_series" "categorical_int_series",
            "categorical_float_series",
            "categorical_string_series",
            "categorical_complex_series",
            "categorical_char",
            "ordinal",
            "bool_series",
            "bool_series2",
            "bool_series3",
            "nullable_bool_series",
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
            "uuid_series_str",
            "str_int_leading_zeros",
            "email_address_str",
            "str_float_non_leading_zeros",
            "str_int_zeros",
            "geometry_series",
            "geometry_series_missing",
            "ip",
            "ip_mixed_v4andv6",
            "ip_missing",
            "uuid_series",
            "uuid_series_missing",
            "file_test_py",
            "file_mixed_ext",
            "file_test_py_missing",
            "image_png",
            "image_png_missing",
            "image_png",
            "image_png_missing",
            "email_address",
            "email_address_missing",
        ],
        Ratio: ["timedelta_series", "timedelta_series_nat"],
        Ordinal: ["ordinal"],
        Generic: [
            "mixed_list[str,int]",
            "mixed_dict",
            "callable",
            "module",
            "bool_nan_series",
            "mixed_integer",
            "mixed_list",
            "mixed",
        ],
    }

    # Empty series
    all = ["empty", "empty_bool", "empty_float", "empty_int64", "empty_object"]
    for key, values in series_map.items():
        all += values
    series_map[Generic] = list(set(all))

    return series_map


@pytest.mark.parametrize("series,type,member", get_contains_cases(get_contains_map))
def test_contains(series, type, member):
    assert contains(series, type, member)

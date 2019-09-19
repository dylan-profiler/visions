import pytest

from tenzing.core import tenzing_model
from tenzing.core.model.types import *

from tests.series import get_series


def get_series_map():
    series_map = {
        tenzing_integer: [
            "int_series",
            "Int64_int_series",
            "np_uint32",
            "int_range",
            "float_series2",
        ],
        tenzing_path: ["path_series_linux", "path_series_windows"],
        tenzing_url: ["url_series"],
        tenzing_float: ["float_series", "float_series3", "float_series4"],
        tenzing_categorical: [
            "categorical_int_series",
            "categorical_float_series",
            "categorical_string_series",
            "categorical_complex_series",
        ],
        tenzing_bool: ["bool_series", "bool_series2", "bool_series3"],
        tenzing_complex: ["complex_series", "complex_series_py"],
        tenzing_datetime: ["timestamp_series", "timestamp_aware_series", "datetime"],
        tenzing_date: ["timestamp_series", "datetime"],
        tenzing_timedelta: ["timedelta_series"],
        tenzing_string: [
            "timestamp_string_series",
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
        ],
        tenzing_geometry: ["geometry_series"],
        tenzing_ip: ["ip"],
        # tenzing_empty: [
        #     "empty",
        #     "empty_float",
        #     "empty_int64",
        #     "empty_object",
        #     "empty_bool",
        # ],
        missing_generic: ["nan_series", "nan_series_2"],
        infinite_generic: ["inf_series"],
    }

    series_map[tenzing_object] = (
        ["mixed_list[str,int]", "mixed_dict", "callable", "module"]
        + series_map[tenzing_string]
        + series_map[tenzing_geometry]
        + series_map[tenzing_path]
        + series_map[tenzing_url]
        + series_map[tenzing_ip]
    )

    # Series with missing values
    series_map[tenzing_date + missing_generic] = (
        series_map[tenzing_date]
        + ["timestamp_series_nat"]
        + series_map[missing_generic]
    )
    series_map[tenzing_datetime + missing_generic] = (
        series_map[tenzing_datetime]
        + ["timestamp_series_nat"]
        + series_map[missing_generic]
    )
    series_map[tenzing_timedelta + missing_generic] = (
        series_map[tenzing_timedelta]
        + ["timedelta_series_nat"]
        + series_map[missing_generic]
    )
    series_map[tenzing_complex + missing_generic] = (
        series_map[tenzing_complex]
        + ["complex_series_py_nan", "complex_series_nan_2", "complex_series_nan"]
        + series_map[missing_generic]
    )
    series_map[tenzing_bool + missing_generic] = (
        series_map[tenzing_bool] + ["bool_nan_series"] + series_map[missing_generic]
    )
    series_map[tenzing_float + missing_generic] = (
        series_map[tenzing_float]
        + ["float_nan_series", "float_series5", "float_series6"]
        + series_map[missing_generic]
    )
    series_map[tenzing_integer + missing_generic] = (
        series_map[tenzing_integer]
        + ["int_nan_series", "Int64_int_nan_series"]
        + series_map[missing_generic]
    )
    series_map[tenzing_string + missing_generic] = (
        series_map[tenzing_string]
        + ["string_num_nan", "string_flt_nan", "string_str_nan", "string_bool_nan"]
        + series_map[missing_generic]
    )

    # Series with inf values
    series_map[tenzing_float + infinite_generic] = (
        series_map[tenzing_float] + ["float_with_inf"] + series_map[infinite_generic]
    )
    series_map[tenzing_integer + infinite_generic] = (
        series_map[tenzing_integer] + ["int_with_inf"] + series_map[infinite_generic]
    )

    # TODO: Series with missing and Inf values

    # Empty series
    all = ["empty", "empty_bool", "empty_float", "empty_int64", "empty_object"]
    for key, values in series_map.items():
        all += values
    series_map[tenzing_model] = list(set(all))

    return series_map


def all_series_included(series_list, series_map):
    """Check that all names are indeed used"""
    used_names = set([name for names in series_map.values() for name in names])
    names = set([series.name for series in series_list])
    if not names == used_names:
        raise ValueError(f"Not all series are used {names ^ used_names}")


def pytest_generate_tests(metafunc):
    if metafunc.function.__name__ == "test_contains":
        _series_map = get_series_map()
        _test_suite = get_series()

        all_series_included(_test_suite, _series_map)

        argsvalues = []
        for item in _test_suite:
            for type, series_list in _series_map.items():
                args = {"id": f"{item.name} x {type}"}
                if item.name not in series_list:
                    args["marks"] = pytest.mark.xfail(raises=AssertionError)

                argsvalues.append(pytest.param(item, type, **args))

        metafunc.parametrize(argnames=["series", "type"], argvalues=argsvalues)


def test_contains(series, type):
    assert series in type


def test_mask(series, type):
    pass
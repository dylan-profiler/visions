import pytest

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
            "Int64_int_nan_series",
        ],
        tenzing_path: ["path_series_linux", "path_series_windows"],
        tenzing_url: ["url_series"],
        tenzing_float: [
            "float_series",
            "float_series3",
            "float_series4",
            "inf_series",
            "nan_series",
            "float_nan_series",
            "float_series5",
            "int_nan_series",
            "nan_series_2",
            "int_with_inf",
            "float_with_inf",
            "float_series6",
        ],
        tenzing_categorical: [
            "categorical_int_series",
            "categorical_float_series",
            "categorical_string_series",
            "categorical_complex_series",
        ],
        tenzing_bool: [
            "bool_series",
            "bool_series2",
            "bool_series3",
            # "nullable_bool_series",
        ],
        tenzing_complex: [
            "complex_series",
            "complex_series_py",
            "complex_series_nan",
            "complex_series_py_nan",
            "complex_series_nan_2",
        ],
        tenzing_datetime: [
            "timestamp_series",
            "timestamp_aware_series",
            "datetime",
            "timestamp_series_nat",
            "date_series_nat",
        ],
        tenzing_date: ["datetime", "date_series_nat"],
        tenzing_timedelta: ["timedelta_series", "timedelta_series_nat"],
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
            "string_str_nan",
            "string_num_nan",
            "string_bool_nan",
            "string_flt_nan",
        ],
        tenzing_geometry: ["geometry_series"],
        tenzing_ip: ["ip"],
    }

    series_map[tenzing_object] = (
        ["mixed_list[str,int]", "mixed_dict", "callable", "module", "bool_nan_series"]
        + series_map[tenzing_string]
        + series_map[tenzing_geometry]
        + series_map[tenzing_path]
        + series_map[tenzing_url]
        + series_map[tenzing_ip]
    )

    # TODO: Series with missing and Inf values

    # Empty series
    all = ["empty", "empty_bool", "empty_float", "empty_int64", "empty_object"]
    for key, values in series_map.items():
        all += values
    series_map[tenzing_generic] = list(set(all))

    return series_map


def all_series_included(series_list, series_map):
    """Check that all names are indeed used"""
    used_names = set([name for names in series_map.values() for name in names])
    names = set([series.name for series in series_list])
    if not names == used_names:
        raise ValueError(f"Not all series are used {names ^ used_names}")


def pytest_generate_tests(metafunc):
    _test_suite = get_series()
    if metafunc.function.__name__ == "test_contains":
        _series_map = get_series_map()

        all_series_included(_test_suite, _series_map)

        argsvalues = []
        for item in _test_suite:
            for type, series_list in _series_map.items():
                args = {"id": f"{item.name} x {type}"}
                if item.name not in series_list:
                    args["marks"] = pytest.mark.xfail(raises=AssertionError)

                argsvalues.append(pytest.param(item, type, **args))

        metafunc.parametrize(argnames=["series", "type"], argvalues=argsvalues)


@pytest.mark.run(order=7)
def test_contains(series, type):
    assert series in type

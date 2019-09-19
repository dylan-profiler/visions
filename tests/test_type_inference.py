import pytest

from tenzing.core import tenzing_model
from tenzing.core.model.typesets import tenzing_complete_set
from tenzing.core.model.types import *
from tests.series import get_series


def get_series_type_map():
    return {
        'int_series': tenzing_integer,
        'categorical_int_series': tenzing_categorical,
        'int_nan_series': tenzing_integer + missing_generic,
        'Int64_int_series': tenzing_integer,
        'Int64_int_nan_series': tenzing_integer + missing_generic,
        'np_uint32': tenzing_integer,
        'int_with_inf': tenzing_float + infinite_generic,
        'int_range': tenzing_integer,
        'float_series': tenzing_float,
        'float_nan_series': tenzing_float + missing_generic,
        'float_series2': tenzing_integer,
        'float_series3': tenzing_float,
        'float_series4': tenzing_float,
        'float_series5': tenzing_float + missing_generic,
        'float_series6': tenzing_float + missing_generic,
        'categorical_float_series': tenzing_categorical,
        'float_with_inf': tenzing_float + infinite_generic,
        'inf_series': infinite_generic,
        'nan_series': missing_generic,
        'nan_series_2': missing_generic,
        'string_series': tenzing_string,
        'categorical_string_series': tenzing_categorical,
        'timestamp_string_series': tenzing_string,
        'string_unicode_series': tenzing_string,
        "string_np_unicode_series": tenzing_string,
        'string_num_nan': tenzing_string + missing_generic,
        'string_num': tenzing_string,
        'string_flt_nan': tenzing_string + missing_generic,
        'string_flt': tenzing_string,
        'string_str_nan': tenzing_string + missing_generic,
        'string_bool_nan': tenzing_string + missing_generic,
        'int_str_range': tenzing_string,
        'string_date': tenzing_string,
        'str_url': tenzing_string,
        'bool_series': tenzing_bool,
        'bool_nan_series': tenzing_bool + missing_generic,
        'bool_series2': tenzing_bool,
        'bool_series3': tenzing_bool,
        'complex_series': tenzing_complex,
        'complex_series_nan': tenzing_complex + missing_generic,
        'complex_series_nan_2': tenzing_complex + missing_generic,
        'complex_series_py_nan': tenzing_complex + missing_generic,
        'complex_series_py': tenzing_complex,
        'categorical_complex_series': tenzing_categorical,
        'timestamp_series': tenzing_datetime,
        'timestamp_series_nat': tenzing_datetime + missing_generic,
        'timestamp_aware_series': tenzing_datetime,
        'datetime': tenzing_date,
        'timedelta_series': tenzing_timedelta,
        'timedelta_series_nat': tenzing_timedelta + missing_generic,
        'geometry_string_series': tenzing_string,
        'geometry_series': tenzing_geometry,
        'path_series_linux': tenzing_path,
        'path_series_linux_str': tenzing_string,
        'path_series_windows': tenzing_path,
        'path_series_windows_str': tenzing_string,
        'url_series': tenzing_url,
        "mixed_list[str,int]": tenzing_object,
        "mixed_dict": tenzing_object,
        "callable": tenzing_object,
        "module": tenzing_object,
        "textual_float": tenzing_string,
        "textual_float_nan": tenzing_string,
        "empty": tenzing_model,
        "empty_object": tenzing_model,
        "empty_float": tenzing_model,
        "empty_bool": tenzing_model,
        "empty_int64": tenzing_model,
        "ip": tenzing_ip,
        "ip_str": tenzing_string,
    }


def pytest_generate_tests(metafunc):
    _test_suite = get_series()
    if metafunc.function.__name__ in ["test_consistency", "test_traversal_mutex"]:
        argsvalues = []
        for series in _test_suite:
            args = {"id": f"{series.name}"}
            argsvalues.append(pytest.param(series, **args))

        metafunc.parametrize(argnames=["series"], argvalues=argsvalues)
    if metafunc.function.__name__ == "test_inference":
        argsvalues = []
        series_type_map = get_series_type_map()
        typeset = tenzing_complete_set()
        for series in _test_suite:
            series_type = series_type_map[series.name]
            for type in typeset.types:
                args = {"id": f"{series.name} x {type}"}
                if type != series_type:
                    args["marks"] = pytest.mark.xfail(raises=AssertionError)
                argsvalues.append(pytest.param(series, type, typeset, **args))
        metafunc.parametrize(argnames=["series", "expected_type", "typeset"], argvalues=argsvalues)


def test_consistency(series):
    typeset = tenzing_complete_set()
    assert series in typeset.get_type_series(series)


def _traverse_relation_graph(series, G, node=tenzing_generic):
    match_types = []
    for tenz_type in G.successors(node):
        if series in tenz_type:
            match_types.append(tenz_type)

    assert (
        len(match_types) < 2
    ), f"types contains should be mutually exclusive {match_types}"
    if len(match_types) == 1:
        return _traverse_relation_graph(series, G, match_types[0])
    else:
        return node


def test_traversal_mutex(series):
    typeset = tenzing_complete_set()
    _traverse_relation_graph(series, typeset.relation_graph)


def test_inference(series, expected_type, typeset):
    assert typeset.get_type_series(series) == expected_type

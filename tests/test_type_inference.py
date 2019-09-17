import pytest

from tenzing.core.model.typesets import tenzing_complete_set
from tenzing.core.typesets import infer_type, traverse_relation_graph
from tenzing.core.model.types import *
from tests.series import get_series


def get_series_map():
    return {
        tenzing_integer: [],
        tenzing_integer + missing_generic: [],
        tenzing_bool: [],
        tenzing_float + missing_generic: [],
    }


def pytest_generate_tests(metafunc):
    if metafunc.function.__name__ == "test_inference":
        _series_map = get_series_map()
        _test_suite = get_series()

        # all_series_included(_test_suite, _series_map)

        argsvalues = []
        for item in _test_suite:
            for type, series_list in _series_map.items():
                args = {"id": f"{item.name} x {type}"}
                if item.name not in series_list:
                    args["marks"] = pytest.mark.xfail()

                argsvalues.append(pytest.param(item, type, **args))

        metafunc.parametrize(argnames=["series", "expected_type"], argvalues=argsvalues)


def test_inference(series, expected_type):
    typeset = tenzing_complete_set()
    series_type = traverse_relation_graph(series, typeset.inheritance_graph)
    inferred_type = infer_type(series_type, series, typeset.relation_graph)
    assert (
        inferred_type is expected_type
    ), f"Inferred type {inferred_type}, expected type {expected_type}"

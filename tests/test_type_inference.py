import pytest

from tenzing.core.model.typesets import tenzing_complete_set
from tenzing.core.model.types import *
from tests.series import get_series, infer_series_type_map


typeset = tenzing_complete_set()


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
        inferred_series_type_map = infer_series_type_map()
        for series in _test_suite:
            expected_type = inferred_series_type_map[series.name]
            for test_type in typeset.types:
                args = {
                    "id": f"{series.name} x {test_type} expected {test_type==expected_type}"
                }
                if test_type != expected_type:
                    args["marks"] = pytest.mark.xfail(raises=AssertionError)
                argsvalues.append(pytest.param(series, test_type, typeset, **args))
        metafunc.parametrize(
            argnames=["series", "expected_type", "typeset"], argvalues=argsvalues
        )


@pytest.mark.run(order=4)
def test_consistency(series):
    assert series in typeset.get_series_type(series)


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


# What does this test? It doesn't explicitly invoke the actual traversal code.
@pytest.mark.run(order=13)
def test_traversal_mutex(series):
    _traverse_relation_graph(series, typeset.relation_graph)


@pytest.mark.run(order=6)
def test_inference(series, expected_type, typeset):
    infered_type = typeset.infer_series_type(series)
    assert infered_type == expected_type

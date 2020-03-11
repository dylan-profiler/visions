import pytest

from visions.typesets import CompleteSet
from visions.types import Generic
from tests.series import get_series, infer_series_type_map


typeset = CompleteSet()


def pytest_generate_tests(metafunc):
    _test_suite = get_series()
    if metafunc.function.__name__ in ["test_consistency", "test_traversal_mutex"]:
        argsvalues = []
        for series in _test_suite:
            args = {"id": series.name}
            argsvalues.append(pytest.param(series, **args))

        metafunc.parametrize(argnames=["series"], argvalues=argsvalues)
    if metafunc.function.__name__ == "test_inference":
        argsvalues = []
        inferred_series_type_map = infer_series_type_map()
        for series in _test_suite:
            expected_type = inferred_series_type_map[series.name]
            for test_type in typeset.types:
                args = {
                    "id": "{name} x {type} expected {expected}".format(
                        name=series.name,
                        type=test_type,
                        expected=test_type == expected_type,
                    )
                }
                difference = test_type != expected_type
                argsvalues.append(
                    pytest.param(series, test_type, typeset, difference, **args)
                )
        metafunc.parametrize(
            argnames=["series", "expected_type", "typeset", "difference"],
            argvalues=argsvalues,
        )


def test_consistency(series):
    assert series in typeset.detect_series_type(series)


def _traverse_relation_graph(series, G, node=Generic):
    match_types = []
    for tenz_type in G.successors(node):
        if series in tenz_type:
            match_types.append(tenz_type)

    assert (
        len(match_types) < 2
    ), "types contains should be mutually exclusive {match_types}".format(
        match_types=match_types
    )
    if len(match_types) == 1:
        return _traverse_relation_graph(series, G, match_types[0])
    else:
        return node


# What does this test? It doesn't explicitly invoke the actual traversal code.
def test_traversal_mutex(series):
    _traverse_relation_graph(series, typeset.relation_graph)


def test_inference(series, expected_type, typeset, difference):
    inferred_type = typeset.infer_series_type(series)
    assert (inferred_type == expected_type) != difference

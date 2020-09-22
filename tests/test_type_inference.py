import pytest

from visions import EmailAddress
from visions.test.series import get_series
from visions.test.series_geometry import get_geometry_series
from visions.types import Generic
from visions.typesets import CompleteSet

typeset = CompleteSet()
typeset += EmailAddress


def pytest_generate_tests(metafunc):
    _test_suite = get_series() + get_geometry_series()
    if metafunc.function.__name__ in ["test_consistency", "test_traversal_mutex"]:
        argsvalues = []
        for series in _test_suite:
            args = {"id": series.name}
            argsvalues.append(pytest.param(series, **args))

        metafunc.parametrize(argnames=["series"], argvalues=argsvalues)


def test_consistency(series):
    detected_type = typeset.detect_type(series)
    message = f"Detected type {detected_type} for series {series.name} but {detected_type}.contains_op(series) -> False"
    assert series in detected_type, message


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

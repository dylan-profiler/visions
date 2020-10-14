import copy
import sys

import pytest

from visions.test.series import get_series
from visions.test.series_geometry import get_geometry_series
from visions.test.utils import sequences_equal
from visions.typesets import CompleteSet


def all_relations_tested(series_map):
    typeset = CompleteSet()

    # Convert data structure for mapping
    series_map_lookup = {}
    for map_to_type, map_from_type, items in series_map:
        try:
            series_map_lookup[map_to_type][map_from_type] = items
        except KeyError:
            series_map_lookup[map_to_type] = {map_from_type: items}

    missing_relations = set()
    for node in typeset.types:
        for relation in node.relations:
            from_type, to_type = relation.related_type, relation.type
            if relation.inferential and (
                to_type not in series_map_lookup
                or from_type not in series_map_lookup[to_type]
                or len(series_map_lookup[to_type][from_type]) == 0
            ):
                missing_relations.add(str(relation))

    if len(missing_relations) > 0:
        raise ValueError(
            "Not all inferential relations are tested {missing_relations}".format(
                missing_relations=missing_relations
            )
        )


def pytest_generate_tests(metafunc):
    _test_suite = get_series()
    _test_suite.update(get_geometry_series())
    if metafunc.function.__name__ in [
        "test_consistency",
        "test_side_effects",
        "test_multiple_inference",
    ]:
        argsvalues = []
        for name, series in _test_suite.items():
            args = {"id": name}
            argsvalues.append(pytest.param(name, series, **args))

        metafunc.parametrize(argnames=["name", "series"], argvalues=argsvalues)


def test_consistency(name, series):
    typeset = CompleteSet()

    if (
        name in ["timedelta_series_nat", "date_series_nat", "timestamp_series_nat"]
        and sys.version_info.major == 3
        and sys.version_info.minor == 7
    ):
        pytest.skip("unsupported configuration")

    initial_type = str(typeset.detect_type(series))
    converted_type = str(typeset.infer_type(series))

    if initial_type != converted_type:
        converted_series = typeset.cast_to_inferred(series.copy(deep=True))

        if hasattr(series, "dtype") and hasattr(converted_series, "dtype"):
            assert (
                series.dtype.kind != converted_series.dtype.kind
                or not sequences_equal(series, converted_series)
            )
        else:
            assert not sequences_equal(series, converted_series)

    else:
        converted_series = typeset.cast_to_inferred(series)
        assert sequences_equal(series, converted_series)


def test_side_effects(name, series):
    reference = series.copy()

    typeset = CompleteSet()
    typeset.detect_type(series)
    typeset.infer_type(series)

    assert sequences_equal(series, reference)


def test_multiple_inference(name, series):
    """
    Notes:
        Copy to prevent possible side effects only for testing.
    """
    ts = CompleteSet()

    inferred_type = str(ts.infer_type(series))

    series_convert = ts.cast_to_inferred(copy.copy(series))

    initial_type_after_convert = str(ts.detect_type(series_convert))
    assert inferred_type == initial_type_after_convert

    series_convert2 = ts.cast_to_inferred(series_convert)

    inferred_type_after_convert = str(ts.infer_type(series_convert2))
    assert initial_type_after_convert == inferred_type_after_convert
    assert sequences_equal(series_convert, series_convert2)

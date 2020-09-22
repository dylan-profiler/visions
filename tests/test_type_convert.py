import sys

import pytest

from visions.test.series import get_series
from visions.test.series_geometry import get_geometry_series
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
    _test_suite = get_series() + get_geometry_series()
    if metafunc.function.__name__ in [
        "test_consistency",
        "test_side_effects",
        "test_multiple_inference",
    ]:
        argsvalues = []
        for series in _test_suite:
            args = {"id": str(series.name)}
            argsvalues.append(pytest.param(series, **args))

        metafunc.parametrize(argnames=["series"], argvalues=argsvalues)


def test_consistency(series):
    typeset = CompleteSet()

    if (
        series.name
        in ["timedelta_series_nat", "date_series_nat", "timestamp_series_nat"]
        and sys.version_info.major == 3
        and sys.version_info.minor == 7
    ):
        pytest.skip("unsupported configuration")

    initial_type = typeset.detect_type(series.copy(deep=True))
    converted_type = typeset.infer_type(series.copy(deep=True))

    if initial_type != converted_type:
        converted_series = typeset.cast_to_inferred(series.copy(deep=True))
        assert series.dtype.kind != converted_series.dtype.kind or not (
            (
                converted_series.eq(series) | (converted_series.isna() & series.isna())
            ).all()
        )
    else:
        converted_series = typeset.cast_to_inferred(series.copy(deep=True))
        assert (
            converted_series.eq(series) | (converted_series.isna() & series.isna())
        ).all()


def test_side_effects(series):
    reference = series.copy()

    typeset = CompleteSet()
    typeset.detect_type(series)
    typeset.infer_type(series)

    # Check if NaN mask is equal
    assert series.notna().eq(reference.notna()).all()
    # Check if NonNaN values are equal
    assert series[series.notna()].eq(reference[reference.notna()]).all()


def test_multiple_inference(series):
    """
    Notes:
        Copy to prevent possible side effects only for testing.
    """
    ts = CompleteSet()

    inferred_type = ts.infer_type(series)

    series_convert = ts.cast_to_inferred(series.copy(deep=True))

    initial_type_after_convert = ts.detect_type(series_convert.copy(deep=True))
    assert inferred_type == initial_type_after_convert

    series_convert2 = ts.cast_to_inferred(series_convert.copy(deep=True))

    inferred_type_after_convert = ts.infer_type(series_convert2.copy(deep=True))
    assert initial_type_after_convert == inferred_type_after_convert

    assert series_convert.isna().eq(series_convert2.isna()).all()
    assert (
        series_convert[series_convert.notna()]
        .eq(series_convert2[series_convert2.notna()])
        .all()
    )

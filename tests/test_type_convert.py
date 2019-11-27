import pytest

from visions.core.implementations.typesets import visions_complete_set
from visions.core.model import TypeRelation

from tests.series import get_series, get_convert_map


def all_relations_tested(series_map):
    typeset = visions_complete_set()

    # Convert data structure for mapping
    series_map_lookup = {}
    for map_to_type, map_from_type, items in series_map:
        try:
            series_map_lookup[map_to_type][map_from_type] = items
        except KeyError:
            series_map_lookup[map_to_type] = {map_from_type: items}

    missing_relations = set()
    for node in typeset.types:
        for relation in node.get_relations():
            from_type, to_type = relation.related_type, relation.type
            if relation.inferential and (
                to_type not in series_map_lookup
                or from_type not in series_map_lookup[to_type]
                or len(series_map_lookup[to_type][from_type]) == 0
            ):
                missing_relations.add(f"{relation}")

    if len(missing_relations) > 0:
        raise ValueError(
            f"Not all inferential relations are tested {missing_relations}"
        )


def pytest_generate_tests(metafunc):
    _test_suite = get_series()
    if metafunc.function.__name__ == "test_relations":
        _series_map = get_convert_map()

        all_relations_tested(_series_map)

        argsvalues = []
        for item in _test_suite:
            for source_type, relation_type, series_list in _series_map:
                if item in relation_type:
                    args = {"id": f"{item.name}: {relation_type} -> {source_type}"}
                    if item.name not in series_list:
                        args["marks"] = pytest.mark.xfail(raises=ValueError)

                    argsvalues.append(
                        pytest.param(source_type, relation_type, item, **args)
                    )

        metafunc.parametrize(
            argnames=["source_type", "relation_type", "series"], argvalues=argsvalues
        )
    if metafunc.function.__name__ in [
        "test_consistency",
        "test_side_effects",
        "test_multiple_inference",
    ]:
        argsvalues = []
        for series in _test_suite:
            args = {"id": f"{series.name}"}
            argsvalues.append(pytest.param(series, **args))

        metafunc.parametrize(argnames=["series"], argvalues=argsvalues)


@pytest.mark.run(order=9)
def test_relations(source_type, relation_type, series):
    relation_gen = (
        rel for rel in source_type.get_relations() if rel.related_type == relation_type
    )
    relation = next(relation_gen)
    if relation.is_relation(series):
        cast_series = relation.transform(series)
        assert (
            cast_series in source_type
        ), f"Relationship {relation} cast {series.values} to {cast_series.values} "
    else:
        raise ValueError("No relation.")


@pytest.mark.run(order=10)
def test_consistency(series):
    typeset = visions_complete_set()

    initial_type = typeset.detect_series_type(series.copy(deep=True))
    converted_type = typeset.infer_series_type(series.copy(deep=True))

    if initial_type != converted_type:
        converted_series = typeset.cast_series(series.copy(deep=True))
        assert series.dtype.kind != converted_series.dtype.kind or not (
            (
                converted_series.eq(series) ^ (converted_series.isna() & series.isna())
            ).all()
        )
    else:
        converted_series = typeset.cast_series(series.copy(deep=True))
        assert (
            converted_series.eq(series) ^ (converted_series.isna() & series.isna())
        ).all()


@pytest.mark.run(order=11)
def test_side_effects(series):
    reference = series.copy()

    typeset = visions_complete_set()
    typeset.detect_series_type(series)
    typeset.infer_series_type(series)

    # Check if NaN mask is equal
    assert series.notna().eq(reference.notna()).all()
    # Check if NonNaN values are equal
    assert series[series.notna()].eq(reference[reference.notna()]).all()


@pytest.mark.run(order=12)
def test_multiple_inference(series):
    """
    Notes:
        Copy to prevent possible side effects only for testing.
    """
    ts = visions_complete_set()

    inferred_type = ts.infer_series_type(series)

    series_convert = ts.cast_series(series.copy(deep=True))

    initial_type_after_convert = ts.detect_series_type(series_convert.copy(deep=True))
    assert inferred_type == initial_type_after_convert

    series_convert2 = ts.cast_series(series_convert.copy(deep=True))

    inferred_type_after_convert = ts.detect_series_type(series_convert2.copy(deep=True))
    assert initial_type_after_convert == inferred_type_after_convert

    assert series_convert.isna().eq(series_convert2.isna()).all()
    assert (
        series_convert[series_convert.notna()]
        .eq(series_convert2[series_convert2.notna()])
        .all()
    )

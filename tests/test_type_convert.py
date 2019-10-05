import os
import warnings

import pytest

from tenzing.core.model import tenzing_complete_set, model_relation
from tenzing.core.model.types import *

from tests.series import get_series, get_convert_map


# TODO: check that all relations are tested


def pytest_generate_tests(metafunc):
    _test_suite = get_series()
    if metafunc.function.__name__ == "test_relations":
        _series_map = get_convert_map()

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
    relation = source_type.get_relations()[relation_type]
    relation = model_relation(source_type, relation_type, **relation._asdict())
    if relation.is_relation(series):
        cast_series = relation.transform(series)
        assert (
            cast_series in source_type
        ), f"Relationship {relation} cast {series.values} to {cast_series.values} "
    else:
        raise ValueError("No relation.")


@pytest.mark.run(order=10)
def test_consistency(series):
    typeset = tenzing_complete_set()

    initial_type = typeset.get_series_type(series.copy(deep=True))
    converted_type = typeset.infer_series_type(series.copy(deep=True))

    if initial_type != converted_type:
        converted_series = typeset.cast_series(series.copy(deep=True))
        print(f"OG {series.to_dict()}, {series.dtype}")
        print(f"Converted {converted_series.to_dict()}, {converted_series.dtype}")
        assert series.dtype != converted_series.dtype or not (
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

    typeset = tenzing_complete_set()
    typeset.get_series_type(series)
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
    ts = tenzing_complete_set()

    inferred_type = ts.infer_series_type(series)

    series_convert = ts.cast_series(series.copy())

    initial_type_after_convert = ts.get_series_type(series_convert.copy())

    inferred_type_after_convert = ts.get_series_type(series_convert.copy())

    series_convert2 = ts.cast_series(series_convert.copy())

    assert inferred_type == initial_type_after_convert
    assert initial_type_after_convert == inferred_type_after_convert
    assert series_convert.isna().eq(series_convert2.isna()).all()
    assert (
        series_convert[series_convert.notna()]
        .eq(series_convert2[series_convert2.notna()])
        .all()
    )

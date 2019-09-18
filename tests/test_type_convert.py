import pytest

from tenzing.core.model import tenzing_complete_set
from tenzing.core.model.types import *

from tests.series import get_series


def get_series_map():
    return [
        (tenzing_integer, tenzing_float, []),
        (tenzing_integer, tenzing_string, []),
        (tenzing_float, tenzing_string, []),
        (tenzing_datetime, tenzing_string, []),
        (tenzing_geometry, tenzing_string, []),
        (tenzing_bool, tenzing_string, []),
    ]


# TODO: check that all series are tested
# TODO: check that all relations are tested
# def all_series_included(series_list, series_map):
#     """Check that all names are indeed used"""
#     used_names = set([name for names in series_map.values() for name in names])
#     names = set([series.name for series in series_list])
#     if not names == used_names:
#         raise ValueError(f"Not all series are used {names ^ used_names}")


def pytest_generate_tests(metafunc):
    _test_suite = get_series()
    if metafunc.function.__name__ == "test_relations":
        _series_map = get_series_map()

        # all_series_included(_test_suite, _series_map)

        argsvalues = []
        for item in _test_suite:
            for source_type, relation_type, series_list in _series_map:
                args = {"id": f"{item.name} x {source_type} x {relation_type}"}
                # if item.name not in series_list:
                #     args["marks"] = pytest.mark.xfail()

                argsvalues.append(
                    pytest.param(source_type, relation_type, item, **args)
                )

        metafunc.parametrize(
            argnames=["source_type", "relation_type", "series"], argvalues=argsvalues
        )
    if metafunc.function.__name__ in ["test_consistency", "test_side_effects", "test_multiple_inference"]:
        argsvalues = []
        for series in _test_suite:
            args = {"id": f"{series.name}"}
            argsvalues.append(pytest.param(series, **args))

        metafunc.parametrize(argnames=["series"], argvalues=argsvalues)


def test_relations(source_type, relation_type, series):
    relation = source_type.get_relations()[relation_type]
    if series in relation_type and relation.is_relation(series):
        cast_series = relation.transform(series)
        assert (
            cast_series in source_type
        ), f"Relationship {relation} cast {series.values} to {cast_series.values} "
    else:
        pass


def test_consistency(series):
    typeset = tenzing_complete_set()
    if typeset.get_type_series(series, convert=True) != typeset.get_type_series(series):
        converted_series = typeset.convert_series(series)
        assert not ((converted_series.eq(series) ^ (converted_series.isna() & series.isna())).all())
    else:
        converted_series = typeset.convert_series(series)
        # Missing values fix
        assert (converted_series.eq(series) ^ (converted_series.isna() & series.isna())).all()


def test_side_effects(series):
    reference = series.copy()

    typeset = tenzing_complete_set()
    typeset.get_type_series(series)
    typeset.get_type_series(series, convert=True)
    typeset.convert_series(series)

    assert series.eq(reference).all()


def test_multiple_inference(series):
    """
    Notes:
        Copy to prevent possible side effects only for testing.
    """
    ts = tenzing_complete_set()

    inferred_type = ts.get_type_series(series, convert=True)

    series_convert = ts.convert_series(series.copy())

    initial_type_after_convert = ts.get_type_series(series_convert.copy())

    inferred_type_after_convert = ts.get_type_series(series_convert.copy(), convert=True)

    series_convert2 = ts.convert_series(series_convert.copy())

    assert inferred_type == initial_type_after_convert
    assert initial_type_after_convert == inferred_type_after_convert
    assert series_convert.eq(series_convert2).all()

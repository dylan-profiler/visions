from typing import Dict, Optional, Set, Tuple, Type

import networkx as nx
import pandas as pd
import pytest

from visions import VisionsBaseType, VisionsTypeset


def all_series_included(series_list, series_map):
    """Check that all names are indeed used"""
    used_names = {name for names in series_map.values() for name in names}
    names = {series.name for series in series_list}
    if not names == used_names:
        unused = names ^ used_names
        # TODO: warning?
        raise ValueError(f"Not all series are included {unused}")


def get_contains_cases(
    _test_suite, _series_map: Dict[Type[VisionsBaseType], Set[str]], typeset
):
    """Parametrize contains tests

    Args:
        mapping: mapping from type to a set of series' identifiers

    Returns:
        the args for the generated tests
    """

    # Include children's series in parent
    reversed_topological_edge_sort = list(
        reversed(list(nx.topological_sort(nx.line_graph(typeset.base_graph))))
    )
    for parent, child in reversed_topological_edge_sort:
        _series_map[parent] |= _series_map[child]

    all_series_included(_test_suite, _series_map)

    argsvalues = []
    for item in _test_suite:
        for type, series_list in _series_map.items():
            args = {"id": f"{item.name} x {type}"}

            member = item.name in series_list
            argsvalues.append(pytest.param(item, type, member, **args))

    return {"argnames": "series,type,member", "argvalues": argsvalues}


def contains(series, type, member):
    return (
        member == (series in type),
        f"{series.name} in {type}; expected {member}, got {series in type}",
    )


def get_inference_cases(_test_suite, inferred_series_type_map, typeset):
    argsvalues = []
    for series in _test_suite:
        expected_type = inferred_series_type_map[series.name]
        for test_type in typeset.types:
            expected = test_type == expected_type
            args = {"id": f"{series.name} x {test_type} expected {expected}"}
            difference = test_type != expected_type
            argsvalues.append(
                pytest.param(series, test_type, typeset, difference, **args)
            )
    return {"argnames": "series,type,typeset,difference", "argvalues": argsvalues}


def infers(series, expected_type, typeset, difference):
    # TODO: include paths on error!
    inferred_type = typeset.infer_type(series)
    return (
        (inferred_type == expected_type) != difference,
        f"inference of {series.name} expected {expected_type} to be {not difference} (typeset={typeset})",
    )
    # return series in inferred_type, f"series should be member of inferred type"


def all_relations_tested(series_map, typeset):
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
            f"Not all inferential relations are tested {missing_relations}"
        )


def get_convert_cases(_test_suite, _series_map, typeset):
    all_relations_tested(_series_map, typeset)

    argsvalues = []
    for item in _test_suite:
        for source_type, relation_type, series_list in _series_map:
            if item in relation_type:
                args = {"id": f"{item.name}: {relation_type} -> {source_type}"}
                member = item.name in series_list
                argsvalues.append(
                    pytest.param(source_type, relation_type, item, member, **args)
                )

    return dict(
        argnames=["source_type", "relation_type", "series", "member"],
        argvalues=argsvalues,
    )


def convert(source_type, relation_type, series, member) -> Tuple[bool, str]:
    relation = source_type.relations.get(relation_type, None)
    is_relation = False if relation is None else relation.is_relation(series, {})

    if not member:
        return (
            (not is_relation),
            f"{source_type}, {relation}, {member}, {series.name}, {series[0]}",
        )
    else:
        # Note that the transformed series is not exactly the cast series
        transformed_series = relation.transform(series, {})

        return (
            is_relation,
            f"Relationship {relation} transformed {series.values} to {transformed_series.values}",
        )


def get_cast_cases(_test_suite, _results):
    argsvalues = []
    for item in _test_suite:
        changed = item.name in _results
        value = _results.get(item.name, "")
        args = {"id": f"{item.name}: {changed}"}
        argsvalues.append(pytest.param(item, value, **args))

    return dict(
        argnames=["series", "expected"],
        argvalues=argsvalues,
    )


def cast(
    series: pd.Series, typeset: VisionsTypeset, expected: Optional[pd.Series] = None
):
    result = typeset.cast_to_inferred(series)
    # TODO: if error also print Path
    if expected is None:
        v = result.equals(series)
        m = f"Series {series.name} cast expected {series.values} (dtype={series.dtype}) (no casting) got {result.values} (dtype={result.dtype})"

        if v:
            v = id(series) == id(result)
            m = f"Series {series.name} memory addresses are not equal, while return value was"
    else:
        v = result.equals(expected)
        m = f"Series {series.name} cast expected {expected.values} (dtype={expected.dtype}) got {result.values} (dtype={result.dtype})"

    return v, m

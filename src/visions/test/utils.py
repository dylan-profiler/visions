from typing import Any, Dict, Iterable, Optional, Sequence, Set, Tuple, Type

import networkx as nx
import pandas as pd
import pytest

from visions import VisionsBaseType, VisionsTypeset

T = Type[VisionsBaseType]


def is_iter(v: Any) -> bool:
    return isinstance(v, Iterable) and not isinstance(v, (str, bytes))


def sequences_equal(s1: Sequence, s2: Sequence) -> bool:
    for v1, v2 in zip(s1, s2):
        if is_iter(v1) and is_iter(v2):
            if not sequences_equal(v1, v2):
                return False
        elif not (pd.isna(v1) and pd.isna(v2)) and not v1 == v2:
            return False

    return True


def all_series_included(
    series_list: Dict[str, Sequence], series_map: Dict[T, Set[str]]
):
    """Check that all names are indeed used"""
    used_names = {name for names in series_map.values() for name in names}
    names = set(series_list.keys())

    if not names == used_names:
        unused = names - used_names
        not_provided = used_names - names
        # TODO: warning?
        if len(unused) > 0:
            raise ValueError(f"{len(unused)} series not included in tests {unused}")
        if len(not_provided) > 0:
            raise ValueError(
                f"{len(not_provided)} series are included, not not provided {not_provided}"
            )


def get_contains_cases(
    _test_suite: Dict[str, Sequence],
    _series_map: Dict[T, Set[str]],
    typeset: VisionsTypeset,
):
    """Parametrize contains tests

    Args:
        _test_suite: mapping from sequence identifiers to sequences
        _series_map: mapping from type to a set of sequence identifiers
        typeset: A VisionsTypeset

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
    for name, item in _test_suite.items():
        for type, series_list in _series_map.items():
            args: Dict[str, Any] = {"id": f"{name} x {type}"}

            member = name in series_list
            argsvalues.append(pytest.param(name, item, type, member, **args))

    return {
        "argnames": ["name", "series", "contains_type", "member"],
        "argvalues": argsvalues,
    }


def contains(name: str, series: Sequence, type: T, member: bool) -> Tuple[bool, str]:
    return (
        member == (series in type),
        f"{name} in {type}; expected {member}, got {series in type}",
    )


def get_inference_cases(
    _test_suite: Dict[str, Sequence],
    inferred_series_type_map: Dict[str, T],
    typeset: VisionsTypeset,
) -> Dict[str, Any]:
    argsvalues = []
    for name, series in _test_suite.items():
        if name not in inferred_series_type_map:
            raise ValueError(
                f"{name} has no defined inference type, please add one to the test case mapping"
            )

        expected_type = inferred_series_type_map[name]
        for test_type in typeset.types:
            expected = test_type == expected_type
            args: Dict[str, Any] = {"id": f"{name} x {test_type} expected {expected}"}
            difference = test_type != expected_type
            argsvalues.append(
                pytest.param(name, series, test_type, typeset, difference, **args)
            )
    return {
        "argnames": "name,series,inference_type,typeset,difference",
        "argvalues": argsvalues,
    }


def infers(
    name: str,
    series: Sequence,
    expected_type: T,
    typeset: VisionsTypeset,
    difference: bool,
) -> Tuple[bool, str]:
    from visions.typesets.typeset import get_type_from_path

    _, paths, _ = typeset.infer(series)
    inferred_type = get_type_from_path(paths)

    # inferred_type = typeset.infer_type(series)
    return (
        (inferred_type == expected_type) != difference,
        f"inference of {name} expected {expected_type} to be {not difference} (typeset={typeset}). Path: {paths}",
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
    for name, item in _test_suite.items():
        for source_type, relation_type, series_list in _series_map:
            for namex in series_list:
                if namex not in _test_suite.keys():
                    raise ValueError(
                        f"{namex} specified in convert_map, but not in provided sequences"
                    )

            if item in relation_type:
                args: Dict[str, Any] = {
                    "id": f"{name}: {relation_type} -> {source_type}"
                }
                member = name in series_list
                argsvalues.append(
                    pytest.param(name, source_type, relation_type, item, member, **args)
                )

    return dict(
        argnames=["name", "source_type", "relation_type", "series", "member"],
        argvalues=argsvalues,
    )


def convert(
    name: str, source_type: T, relation_type: T, series: Sequence, member: bool
) -> Tuple[bool, str]:
    relation = source_type.relations.get(relation_type, None)
    is_relation = False if relation is None else relation.is_relation(series, {})

    if not member:
        return (
            (not is_relation),
            f"{source_type}, {relation}, {member}, {name}, {series}",
        )
    else:
        # Note that the transformed series is not exactly the cast series
        transformed_series = list(relation.transform(series, {}))

        return (
            is_relation,
            f"Relationship {relation} for {series} tested false (but shouldn't have). "
            f"Transform result would have been {transformed_series}",
        )


def get_cast_cases(_test_suite: Dict[str, Sequence], _results: Dict) -> Dict:
    argsvalues = []
    for name, item in _test_suite.items():
        changed = name in _results
        value = _results.get(name, "")
        args: Dict[str, Any] = {"id": f"{name}: {changed}"}
        argsvalues.append(pytest.param(name, item, value, **args))

    return dict(
        argnames=["name", "series", "expected"],
        argvalues=argsvalues,
    )


def cast(
    name: str,
    series: Sequence,
    typeset: VisionsTypeset,
    expected: Optional[pd.Series] = None,
) -> Tuple[bool, str]:
    result = typeset.cast_to_inferred(series)
    # TODO: if error also print Path
    if expected is None:
        v = sequences_equal(result, series)
        m = f"Series {name} cast expected {series} (no casting) got {result}"

        if v:
            v = id(series) == id(result)
            m = f"Series {name} memory addresses are not equal, while return value was"
    else:
        v = sequences_equal(result, expected)
        m = f"Series {name} cast expected {expected} got {result}"

    return v, m

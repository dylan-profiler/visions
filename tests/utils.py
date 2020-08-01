from typing import Dict, Set, Tuple, Type

import networkx as nx
import pytest

from visions import VisionsBaseType


def all_series_included(series_list, series_map):
    """Check that all names are indeed used"""
    used_names = set([name for names in series_map.values() for name in names])
    names = set([series.name for series in series_list])
    if not names == used_names:
        raise ValueError(
            "Not all series are included {unused}".format(unused=names ^ used_names)
        )


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
    inferred_series_type_map = inferred_series_type_map
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
    return {"argnames": "series,type,typeset,difference", "argvalues": argsvalues}


def infers(series, expected_type, typeset, difference):
    inferred_type = typeset.infer_type(series)
    return (
        (inferred_type == expected_type) != difference,
        f"inference of {series.name} expected {expected_type} to be {difference} (typeset={typeset})",
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
            "Not all inferential relations are tested {missing_relations}".format(
                missing_relations=missing_relations
            )
        )


def get_convert_cases(_test_suite, _series_map, typeset):
    all_relations_tested(_series_map, typeset)

    argsvalues = []
    for item in _test_suite:
        for source_type, relation_type, series_list in _series_map:
            if item in relation_type:
                args = {
                    "id": "{name}: {relation_type} -> {source_type}".format(
                        name=item.name,
                        relation_type=relation_type,
                        source_type=source_type,
                    )
                }
                member = item.name in series_list
                argsvalues.append(
                    pytest.param(source_type, relation_type, item, member, **args)
                )

    return dict(
        argnames=["source_type", "relation_type", "series", "member"],
        argvalues=argsvalues,
    )


def convert(source_type, relation_type, series, member) -> Tuple[bool, str]:
    relation_gen = (
        rel for rel in source_type.relations if rel.related_type == relation_type
    )
    relation = next(relation_gen)

    is_relation = relation.is_relation(series)

    if not member:
        return (
            (not is_relation),
            f"{source_type}, {relation}, {member}, {series.name}, {series[0]}",
        )
    else:
        cast_series = relation.transform(series)

        return (
            (is_relation and cast_series in source_type),
            "Relationship {relation} cast {series_values} to {cast_values}".format(
                relation=relation,
                series_values=series.values,
                cast_values=cast_series.values,
            ),
        )

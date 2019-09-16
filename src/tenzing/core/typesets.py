import warnings

import pandas as pd
import networkx as nx
from networkx.drawing.nx_agraph import write_dot

from tenzing.core.model.types.tenzing_generic import tenzing_generic
from tenzing.core.containers import MultiContainer, TypeC


def build_relation_graph(nodes: set) -> nx.DiGraph:
    """Constructs a traversible relation graph between tenzing types
    Builds a type relation graph from a collection of root and derivative nodes. Usually
    root nodes correspond to the baseline numpy types found in pandas while derivative
    nodes correspond to subtypes with a defined relation.

    Args:
        nodes : List[tenzing_type]
            A list of tenzing_types considered at the root of the relations graph.

    Returns:
        networkx DiGraph
            A directed graph of type relations for the provided nodes.
    """
    relation_graph = nx.DiGraph()
    relation_graph.add_nodes_from(nodes)
    relation_graph.add_edges_from(
        (node.edge[0], node.edge[1], {"relationship": node})
        for s_node in nodes
        for to_node, node in s_node.get_relations().items()
    )
    undefined_nodes = set(relation_graph.nodes) - nodes
    relation_graph.remove_nodes_from(undefined_nodes)
    check_graph_constraints(relation_graph, nodes)
    return relation_graph


def check_graph_constraints(relation_graph, nodes):
    relation_graph.remove_nodes_from(list(nx.isolates(relation_graph)))

    orphaned_nodes = nodes - set(relation_graph.nodes)
    if orphaned_nodes:
        warnings.warn(
            f"{orphaned_nodes} were isolates in the type relation map and consequently orphaned. Please add some mapping to the orphaned nodes."
        )

    cycles = list(nx.simple_cycles(relation_graph))
    if len(cycles) > 0:
        warnings.warn(f"Cyclical relations between types {cycles} detected")


def traverse_relation_graph(series, G, node=tenzing_generic):
    match_types = []
    for tenz_type in G.successors(node):
        if series in tenz_type:
            match_types.append(tenz_type)

    if len(match_types) == 1:
        return traverse_relation_graph(series, G, match_types[0])
    elif len(match_types) > 1:
        raise ValueError(f"types contains should be mutually exclusive {match_types}")
    else:
        return node


def get_type_inference_path(base_type, series, G, path=[]):
    path.append(base_type)

    # TODO: assert all relationships
    for tenz_type in G.successors(base_type):
        if G[base_type][tenz_type]["relationship"].is_relation(series):
            new_series = G[base_type][tenz_type]["relationship"].transform(series)
            return get_type_inference_path(tenz_type, new_series, G, path)
    return path, series


def infer_type(base_type, series, G):
    path, _ = get_type_inference_path(base_type, series, G)
    return path[-1]


def cast_series_to_inferred_type(base_type, series, G):
    _, series = get_type_inference_path(base_type, series, G)
    return series


def detect_series_container(series, containers):
    series_containers = [container for container in containers if series in container]
    container = MultiContainer(series_containers) if len(series_containers) > 1 else series_containers[0]
    return container


# TODO: Should be container...
# class Type:
#     def __init__(self, container, base_type):
#         self.container = container
#         self.base_type = base_type
#
#     def contains_op(self, series):
#         if series in self.container:
#             return series in self.base_type
#         else:
#             return False
#
#     def transform(self, series):
#         container_mask = self.container.mask(series)
#         series[container_mask] = self.base_type.cast_op(series[container_mask])
#         return series
#
#     def __repr__(self) -> str:
#         return f"{self.container}[{self.base_type}]"
#
#     def __contains__(self, series) -> bool:
#         try:
#             return self.contains_op(series)
#         except Exception:
#             return False


class tenzingTypeset(object):
    """
    A collection of tenzing_types with an associated relationship map between them.

    Attributes
    ----------
    types: frozenset
        The collection of tenzing types which are derived either from a base_type or themselves
    """

    def __init__(self, containers: list, types: list):
        self.column_container_map = {}
        self.column_base_type_map = {}
        self.column_type_map = {}

        self.relation_graph = build_relation_graph(set(types) | {tenzing_generic})
        self.types = frozenset(self.relation_graph.nodes)
        self.containers = containers

    def prep(self, df):
        self.column_container_map = {col: self.detect_series_container(df[col]) for col in df.columns}
        self.column_base_type_map = {col: self._get_column_type(df[col]) for col in df.columns}
        self.column_type_map = {MultiContainer(self.column_container_map[col] + TypeC(self.column_base_type_map[col]))
                                for col in df.columns}

    def detect_series_container(self, series):
        self.column_base_type_map[series.name] = detect_series_container(series, self.containers)
        return self.column_base_type_map[series.name]

    def get_containerized_series(self, series):
        container = self.detect_series_container(series)
        return container.transform(series)

    def infer_types(self, df: pd.DataFrame):
        self.prep(df)
        return {col: self.infer_series_type(df[col]) for col in df.columns}

    def cast_to_inferred_types(self, df: pd.DataFrame):
        self.prep(df)
        return pd.DataFrame(
            {col: self.cast_series_to_inferred_type(df[col]) for col in df.columns}
        )

    def infer_series_type(self, series: pd.Series):
        containerized_series = self.get_containerized_series(series)
        base_type = infer_type(self.column_base_type_map[series.name], containerized_series, self.relation_graph)
        return base_type

    def cast_series_to_inferred_type(self, series: pd.Series) -> pd.Series:
        mask = self.column_container_map[series.name].mask(series)
        series.loc[mask] = cast_series_to_inferred_type(self.column_base_type_map[series.name],
                                                        series[mask],
                                                        self.relation_graph)
        return series

    def _get_column_type(self, series: pd.Series):
        # walk the relation_map to determine which is most uniquely specified
        return traverse_relation_graph(series, self.relation_graph)

    def write_dot(self, file_name="graph_relations.dot") -> None:
        G = self.relation_graph.copy()
        G.graph["node"] = {"shape": "box", "color": "red"}

        write_dot(G, file_name)

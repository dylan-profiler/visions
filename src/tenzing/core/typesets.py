import warnings

import pandas as pd
import networkx as nx
from networkx.drawing.nx_agraph import write_dot
from tenzing.core.model_implementations.compound_type import CompoundType

from tenzing.core.model_implementations.types.tenzing_generic import tenzing_generic
from tenzing.core.summaries.dataframe_summary import dataframe_summary
from tenzing.core.summary import type_summary_ops, Summary


def build_relation_graph(nodes):
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

    check_graph_constraints(relation_graph, nodes)
    return relation_graph


def check_graph_constraints(relation_graph, nodes):
    undefined_nodes = set(relation_graph.nodes) - nodes
    relation_graph.remove_nodes_from(undefined_nodes)
    relation_graph.remove_nodes_from(list(nx.isolates(relation_graph)))

    orphaned_nodes = [n for n in nodes if n not in set(relation_graph.nodes)]
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


def get_type_inference_path(base_type, series, G, path=None):
    if path is None:
        path = []
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


class tenzingTypeset(object):
    """
    A collection of tenzing_types with an associated relationship map between them.

    Attributes
    ----------
    types: frozenset
        The collection of tenzing types which are derived either from a base_type or themselves
    """

    def __init__(self, types: list):
        tps = set(types) | {tenzing_generic}
        # TODO: make compound work with base
        self.types = frozenset(
            [x.base_type if isinstance(x, CompoundType) else x for x in tps]
        )
        self.relation_graph = build_relation_graph(self.types)
        self.column_summary = {}

    def prep(self, df):
        # TODO: improve this (no new attributes outside of __init__)
        self.column_type_map = {
            col: self._get_column_type(df[col]) for col in df.columns
        }

    def summarize(self, df):
        # TODO: defined over typeset
        summary = Summary(type_summary_ops)

        self.prep(df)
        summary = {
            col: summary.summarize_series(df[col], self.column_type_map[col])
            for col in df.columns
        }
        self.column_summary = summary
        return self.column_summary

    def summary_report(self, df):
        general_summary = dataframe_summary(df)
        column_summary = self.summarize(df)
        return {
            "types": self.column_type_map,
            "columns": column_summary,
            "general": general_summary,
        }

    def infer_types(self, df):
        self.prep(df)
        return {col: self.infer_series_type(df[col]) for col in df.columns}

    def cast_to_inferred_types(self, df):
        return pd.DataFrame(
            {col: self.cast_series_to_inferred_type(df[col]) for col in df.columns}
        )

    def infer_series_type(self, series):
        return infer_type(
            self.column_type_map[series.name], series, self.relation_graph
        )

    def cast_series_to_inferred_type(self, series):
        _, series = get_type_inference_path(
            self.column_type_map[series.name], series, self.relation_graph
        )
        return series

    def _get_column_type(self, series):
        # walk the relation_map to determine which is most uniquely specified
        return traverse_relation_graph(series, self.relation_graph)

    def write_dot(self):
        G = self.relation_graph.copy()
        G.graph["node"] = {"shape": "box", "color": "red"}

        write_dot(G, "graph_relations.dot")

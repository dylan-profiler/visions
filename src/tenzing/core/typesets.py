import operator
import warnings
from functools import reduce
from typing import Union, Type

import pandas as pd
import networkx as nx

from tenzing.core.models import MultiModel, tenzing_model
from tenzing.utils.graph import output_graph


def build_relation_graph(nodes: set) -> nx.DiGraph:
    """Constructs a traversible relation graph between tenzing types
    Builds a type relation graph from a collection of root and derivative nodes. Usually
    root nodes correspond to the baseline numpy types found in pandas while derivative
    nodes correspond to subtypes with a defined relation.

    Args:
        nodes:  A list of tenzing_types considered at the root of the relations graph.

    Returns:
        A directed graph of type relations for the provided nodes.
    """
    style_map = {True: "dashed", False: "solid"}
    relation_graph = nx.DiGraph()
    relation_graph.add_nodes_from(nodes)
    relation_graph.add_edges_from(
        (
            node.friend_model,
            node.model,
            {"relationship": node, "style": style_map[node.conversion]},
        )
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


# Infer type without conversion
def traverse_relation_graph(series, G, node=tenzing_model) -> Type[tenzing_model]:
    # DFS
    for tenz_type in G.successors(node):
        # TODO: speed gain by not considering "dashed"
        if series in tenz_type:
            return traverse_relation_graph(series, G, tenz_type)

    return node


# Infer type with conversion
def get_type_inference_path(base_type, series, G, path=[]):
    path.append(base_type)

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


class tenzingTypeset(object):
    """
    A collection of tenzing_types with an associated relationship map between them.

    Attributes:
        types: The collection of tenzing types which are derived either from a base_type or themselves
    """

    def __init__(self, partitioners: list, types: list):
        self.partitioners = partitioners

        self.column_partitioner_map = {}
        self.column_base_type_map = {}
        self.column_type_map = {}

        self.relation_graph = build_relation_graph(set(types))
        self.types = frozenset(self.relation_graph.nodes)

    def get_partition_types(self, series: pd.Series):
        parts = []
        if series.empty:
            return tenzing_model

        for partitioner in self.partitioners:
            mask = partitioner.mask(series)
            if mask.any():
                new_series = series[mask]
                node = traverse_relation_graph(new_series, self.relation_graph, partitioner)
                parts.append(node)

        if len(parts) == 0:
            return tenzing_model
        else:
            return reduce(operator.add, parts)

    # New API
    def get_type_series(
        self, series: pd.Series, convert=False
    ) -> Union[tenzing_model, MultiModel]:
        if convert:
            return self.infer_series_type(series)
        else:
            return self.get_partition_types(series)

    def convert_series(self, series: pd.Series) -> pd.Series:
        return self.cast_series_to_inferred_type(series)

    def infer_series_type(self, series: pd.Series):
        # containerized_series = self.get_containerized_series(series)
        base_type = infer_type(
            self.column_base_type_map[series.name], series, self.relation_graph
        )
        return base_type

    def cast_series_to_inferred_type(self, series: pd.Series) -> pd.Series:
        # TODO: copy if needed!
        mask = self.column_partitioner_map[series.name].mask(series)
        series.loc[mask] = cast_series_to_inferred_type(
            self.column_base_type_map[series.name], series[mask], self.relation_graph
        )
        return series

    # def _get_column_type(self, series: pd.Series):
    #     # walk the relation_map to determine which is most uniquely specified
    #     return traverse_relation_graph(series, self.relation_graph)

    def _get_ancestors(self, node):
        if isinstance(node, MultiModel):
            return {mdl for x in node.models for mdl in nx.ancestors(self.relation_graph, x)}
        else:
            return nx.ancestors(self.relation_graph, node)

    def output(self, file_name) -> None:
        G = self.relation_graph.copy()
        G.graph["node"] = {"shape": "box", "color": "red"}

        output_graph(G, file_name)

    def plot_graph(self, dpi=800):
        import matplotlib.pyplot as plt
        import matplotlib.image as mpimg
        import tempfile

        G = self.relation_graph.copy()
        G.graph["node"] = {"shape": "box", "color": "red"}
        with tempfile.NamedTemporaryFile(suffix=".png") as temp_file:
            p = nx.drawing.nx_pydot.to_pydot(G)
            p.write_png(temp_file.name)
            img = mpimg.imread(temp_file.name)
            plt.figure(dpi=dpi)
            plt.imshow(img)

import operator
import warnings
from functools import reduce
from typing import Union, Type, Tuple, List

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


def check_graph_constraints(relation_graph: nx.DiGraph, nodes: set) -> None:
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
def traverse_relation_graph(series: pd.Series, G: nx.DiGraph, node: Type[tenzing_model] = tenzing_model) -> Type[tenzing_model]:
    # DFS
    for tenz_type in G.successors(node):
        # TODO: speed gain by not considering "dashed"
        if series in tenz_type:
            return traverse_relation_graph(series, G, tenz_type)

    return node


# Infer type with conversion
def get_type_inference_path(base_type: Type[tenzing_model], series: pd.Series, G: nx.DiGraph, path=None) -> Tuple[List[Type[tenzing_model]], pd.Series]:
    if path is None:
        path = []

    path.append(base_type)

    for tenz_type in G.successors(base_type):
        if G[base_type][tenz_type]["relationship"].is_relation(series):
            # print(f"cast {base_type} to {tenz_type}")
            new_series = G[base_type][tenz_type]["relationship"].transform(series)
            return get_type_inference_path(tenz_type, new_series, G, path)
    return path, series


def infer_type(base_type: Type[tenzing_model], series: pd.Series, G: nx.DiGraph) -> Type[tenzing_model]:
    path, _ = get_type_inference_path(base_type, series, G)
    return path[-1]


def cast_series_to_inferred_type(base_type: Type[tenzing_model], series: pd.Series, G: nx.DiGraph) -> pd.Series:
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

        self.relation_graph = build_relation_graph(set(types))
        self.types = frozenset(self.relation_graph.nodes)

    def get_partition_types(
        self, series: pd.Series, convert=False
    ) -> Union[Type[tenzing_model], MultiModel]:
        if series.empty:
            return tenzing_model

        parts = []
        for partitioner in self.partitioners:
            mask = partitioner.mask(series)
            if mask.any():
                new_series = series[mask]
                if convert:
                    node = infer_type(partitioner, new_series, self.relation_graph)
                else:
                    node = traverse_relation_graph(
                        new_series, self.relation_graph, partitioner
                    )
                parts.append(node)

        if len(parts) == 0:
            return tenzing_model
        else:
            return reduce(operator.add, parts)

    # New API
    def get_type_series(
        self, series: pd.Series, convert=False
    ) -> Union[Type[tenzing_model], MultiModel]:
        series_type = self.get_partition_types(series, convert)
        return series_type

    def convert_series(self, series: pd.Series) -> pd.Series:
        # TODO: document that this has Side effects!
        series_type = self.get_type_series(series)
        convert_type = self.get_type_series(series, True)

        if series_type == convert_type:
            return series

        cast_from = series_type.get_models()

        cast_to = convert_type.get_models()

        # For each partition...
        for type_from, type_to in zip(cast_from, cast_to):
            mask = type_from.mask(series)
            res = cast_series_to_inferred_type(
                type_from, series[mask], self.relation_graph
            )
            series.loc[mask] = res
        return series

    def _get_ancestors(self, node: Type[tenzing_model]) -> set:
        return {
            mdl for x in node.get_models() for mdl in nx.ancestors(self.relation_graph, x)
        }

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

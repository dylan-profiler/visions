import warnings
from typing import Type, Tuple, List

import pandas as pd
import networkx as nx

from tenzing.core.model.models import tenzing_model
from tenzing.utils.graph import output_graph
from tenzing.core.model.types import tenzing_generic


def build_relation_graph(nodes: set) -> nx.DiGraph:
    """Constructs a traversable relation graph between tenzing types
    Builds a type relation graph from a collection of root and derivative nodes. Usually
    root nodes correspond to the baseline numpy types found in pandas while derivative
    nodes correspond to subtypes with a defined relation.

    Args:
        nodes:  A list of tenzing_types considered at the root of the relations graph.

    Returns:
        A directed graph of type relations for the provided nodes.
    """
    style_map = {True: "dashed", False: "solid", None: "dotted"}
    relation_graph = nx.DiGraph()
    relation_graph.add_nodes_from(nodes)
    relation_graph.add_edges_from(
        (*node.edge, {"relationship": node, "style": style_map[node.inferential]})
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
def traverse_relation_graph(series: pd.Series,
                            G: nx.DiGraph,
                            node: Type[tenzing_model] = tenzing_generic
                            ) -> Type[tenzing_model]:
    """Depth First Search traversal. There should be at most one successor that contains the series.

    Args:
        series: the Series to check
        G: the Graph to traverse
        node: the current node

    Returns:
        The most specialist node matching the series.
    """
    for tenz_type in G.successors(node):
        # TODO: speed gain by not considering "dashed"
        if series in tenz_type:
            return traverse_relation_graph(series, G, tenz_type)

    return node


# Infer type with conversion
def get_type_inference_path(
    base_type: Type[tenzing_model], series: pd.Series, G: nx.DiGraph, path=None
) -> Tuple[List[Type[tenzing_model]], pd.Series]:
    """

    Args:
        base_type:
        series:
        G:
        path:

    Returns:

    """
    if path is None:
        path = []
    path.append(base_type)

    for tenz_type in G.successors(base_type):
        if G[base_type][tenz_type]["relationship"].is_relation(series):
            new_series = G[base_type][tenz_type]["relationship"].transform(series)
            return get_type_inference_path(tenz_type, new_series, G, path)
    return path, series


def infer_type(
    base_type: Type[tenzing_model], series: pd.Series, G: nx.DiGraph
) -> Type[tenzing_model]:
    """

    Args:
        base_type:
        series:
        G:

    Returns:

    """
    # TODO: path is never used...
    path, _ = get_type_inference_path(base_type, series, G)
    return path[-1]


def cast_series_to_inferred_type(
    base_type: Type[tenzing_model], series: pd.Series, G: nx.DiGraph
) -> pd.Series:
    """

    Args:
        base_type:
        series:
        G:

    Returns:

    """
    _, series = get_type_inference_path(base_type, series, G)
    return series


# class TenzingType:
#     def __init__(self, partitioner, base_type):
#         self.partitioner = partitioner
#         self.base_type = base_type
#
#     def contains_op(self, series):
#         if series in self.partitioner:
#             return series in self.base_type
#         else:
#             return False
#
#     def transform(self, series):
#         series = series.copy()
#         partitioner_mask = self.partitioner.mask(series)
#         series.loc[partitioner_mask] = self.base_type.cast_op(series[partitioner_mask])
#         return series
#
#     def __repr__(self):
#         return f"{str(self.partitioner)}[{self.base_type}]"


class tenzingTypeset(object):
    """
    A collection of tenzing_types with an associated relationship map between them.

    Attributes:
        types: The collection of tenzing types which are derived either from a base_type or themselves
        partitioners: ...
        relation_graph: ...
    """

    def __init__(self, types: list):
        """

        Args:
            types:
        """
        self.column_type_map = {}
        # self.partitioners = set(partitioners)

        self.relation_graph = build_relation_graph(set(types) | {tenzing_generic})
        self.types = frozenset(self.relation_graph.nodes)

    def prep(self, df):
        self.column_type_map = {
            column: self.get_series_type(df[column]) for column in df.columns
        }

    def get_series_type(self, series: pd.Series) -> Type[tenzing_model]:
        """
        """
        # partitioner = get_series_partitioner(series, self.partitioners)
        # series = partitioner.partition(series)
        base_type = traverse_relation_graph(series, self.relation_graph)
        # return TenzingType(partitioner, base_type)
        return base_type

    def infer_series_type(self, series: pd.Series) -> Type[tenzing_model]:
        col_type = self.column_type_map[series.name]
        # series = col_type.partitioner.partition(series)
        inferred_base_type = infer_type(col_type.base_type, series, self.relation_graph)
        # return TenzingType(col_type.partitioner, inferred_base_type)
        return inferred_base_type

    def cast_series(self, series: pd.Series) -> pd.Series:
        """

        Args:
            series:

        Returns:

        """
        series_type = self.infer_series_type(series)
        return series_type.transform(series)

    def cast_to_inferred_types(self, df: pd.DataFrame) -> pd.DataFrame:
        self.prep(df)
        return pd.DataFrame({col: self.cast_series(df[col]) for col in df.columns})

    def _get_ancestors(self, node: Type[tenzing_model]) -> set:
        """

        Args:
            node:

        Returns:

        """
        return {
            mdl
            for x in node.get_models()
            for mdl in nx.ancestors(self.relation_graph, x)
        }

    def output_graph(self, file_name) -> None:
        """

        Args:
            file_name:

        Returns:

        """
        G = self.relation_graph.copy()
        G.graph["node"] = {"shape": "box", "color": "red"}

        output_graph(G, file_name)

    def plot_graph(self, dpi=800):
        """

        Args:
            dpi:

        Returns:

        """
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

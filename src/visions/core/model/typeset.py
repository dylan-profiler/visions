import warnings
from typing import Type, Tuple, List, Dict, Iterable

import pandas as pd
import networkx as nx

from visions.core.model import TypeRelation
from visions.core.model.type import VisionsBaseType
from visions.utils.graph import output_graph
from visions.core.model.visions_generic import visions_generic


def build_graph(nodes: set) -> Tuple[nx.DiGraph, nx.DiGraph]:
    """Constructs a traversable relation graph between visions types
    Builds a type relation graph from a collection of root and derivative nodes. Usually
    root nodes correspond to the baseline numpy types found in pandas while derivative
    nodes correspond to subtypes with a defined relation.

    Args:
        nodes:  A list of vision_types considered at the root of the relations graph.

    Returns:
        A directed graph of type relations for the provided nodes.
    """

    def get_relations(node, nodes):
        return (
            relation
            for relation in node.get_relations()
            if relation.related_type in nodes
        )

    style_map = {True: "dashed", False: "solid"}
    relation_graph = nx.DiGraph()
    relation_graph.add_nodes_from(nodes)

    noninferential_edges = []

    for node in nodes:
        for relation in node.get_relations():
            if relation.related_type not in nodes:
                warnings.warn(
                    f"Provided relations included mapping from {relation.related_type} to {relation.type} but {relation.related_type} was not included in the provided list of nodes"
                )

            relation_graph.add_edge(
                relation.related_type,
                relation.type,
                relationship=relation,
                style=style_map[relation.inferential],
            )

            if not relation.inferential:
                noninferential_edges.append((relation.related_type, relation.type))

    check_graph_constraints(relation_graph)
    return relation_graph, relation_graph.edge_subgraph(noninferential_edges)


def check_graph_constraints(relation_graph: nx.DiGraph) -> None:
    """Validates a relation_graph is appropriately constructed

    Args:
        relation_graph: A directed graph representing the set of relations between type nodes.

    """
    check_isolates(relation_graph)
    check_cycles(relation_graph)


def check_isolates(graph: nx.DiGraph) -> None:
    """Check for orphaned nodes.

    Args:
        graph: the graph to check

    """
    nodes = set(graph.nodes)
    isolates = list(set(nx.isolates(graph)) - {visions_generic})  # root can be isolate
    graph.remove_nodes_from(isolates)
    orphaned_nodes = nodes - set(graph.nodes)
    if orphaned_nodes:
        warnings.warn(
            f"{orphaned_nodes} were isolates in the type relation map and consequently\
                      orphaned. Please add some mapping to the orphaned nodes."
        )


def check_cycles(graph: nx.DiGraph) -> None:
    """Check for cycles and warn if one is found

    Args:
        graph: the graph to check

    """
    cycles = list(nx.simple_cycles(graph))
    if len(cycles) > 0:
        warnings.warn(f"Cyclical relations between types {cycles} detected")


def traverse_graph(
    series: pd.Series, graph: nx.DiGraph, node: Type[VisionsBaseType] = visions_generic
) -> Type[VisionsBaseType]:
    """Depth First Search traversal. There should be at most one successor that contains the series.

    Args:
        series: the Series to check
        graph: the Graph to traverse
        node: the current node

    Returns:
        The most uniquely specified node matching the series.
    """
    for vision_type in graph.successors(node):
        if series in vision_type:
            return traverse_graph(series, graph, vision_type)

    return node


def traverse_graph_inference(
    node: Type[VisionsBaseType], series: pd.Series, graph: nx.DiGraph, path=None
) -> Tuple[List[Type[VisionsBaseType]], pd.Series]:
    """Depth First Search traversal. There should be at most one successor that contains the series.

    Args:
        series: the Series to check
        graph: the Graph to traverse
        node: the current node
        path: the path so far

    Returns:
        The most uniquely specified node matching the series.
    """
    if path is None:
        path = []

    path.append(node)

    for vision_type in graph.successors(node):
        if graph[node][vision_type]["relationship"].is_relation(series):
            new_series = graph[node][vision_type]["relationship"].transform(series)
            return traverse_graph_inference(vision_type, new_series, graph, path)

    return path, series


def traverse_graph_inference_sample(
    node: Type[VisionsBaseType],
    series: pd.Series,
    graph: nx.DiGraph,
    sample_size: int = 10,
    sample=None,
    path=None,
) -> Tuple[List[Type[VisionsBaseType]], pd.Series]:
    """Depth First Search traversal. There should be at most one successor that contains the series.

    Args:
        series: the Series to check
        graph: the Graph to traverse
        node: the current node
        path: the path so far

    Returns:
        The most uniquely specified node matching the series.
    """
    if path is None:
        path = []
    if sample is None:
        sample = series.sample(sample_size)

    path.append(node)

    for vision_type in graph.successors(node):
        if graph[node][vision_type]["relationship"].is_relation(sample):
            try:
                series = graph[node][vision_type]["relationship"].transform(series)
            except Exception:
                # TODO: alternatively, increase sample size
                raise ValueError(
                    f"Sample size for inference {sample_size} was too small"
                )
            return traverse_graph_inference_sample(
                vision_type, series, graph, sample_size, sample, path
            )

    return path, series


# TODO: remove or use
# def cast_along_path(
#     series: pd.Series, path: List[Type[VisionsBaseType]], graph: nx.DiGraph
# ) -> pd.Series:
#     """Successively cast series along a path of visions types.
#
#     Args:
#         series: the Series to cast
#         path: the path to follow
#         graph: the graph
#
#     Returns:
#         The casted series
#     """
#     if len(path) <= 1:
#         raise ValueError("path should at least contain 2 values")
#
#     new_series = series.copy()
#
#     for from_type, to_type in zip(path, path[1:]):
#         new_series = graph[from_type][to_type]["relationship"].transform(new_series)
#
#     return new_series


def infer_type_path(
    series: pd.Series,
    G: nx.DiGraph,
    base_type: Type[VisionsBaseType] = visions_generic,
    sample_size: int = 10,
) -> Tuple[List[Type[VisionsBaseType]], pd.Series]:
    # TODO: Try sample, Except do this
    if sample_size >= len(series):
        path, new_series = traverse_graph_inference(base_type, series, G)
        return path, new_series

    # Sample a part of the series
    series_sample = series.sample(sample_size)

    # Infer the type
    path, new_series_sample = traverse_graph_inference(base_type, series_sample, G)

    # Cast the full series
    from_type = to_type = path[0]
    for i, to_type in enumerate(path[1:]):
        if not G[from_type][to_type]["relationship"].is_relation(series):
            break
        series = G[from_type][to_type]["relationship"].transform(series)
        from_type = to_type

    return path[0 : (i + 1)], series


class VisionsTypeset(object):
    """
    A set of visions types with an associated relationship map between them.

    Attributes:
        types: The collection of vision types which are derived either from a base_type or themselves
        base_graph: the graph with relations to parent types
        relation_graph: the graph with relations to the parent types and mapping relations
    """

    def __init__(self, types: set):
        """
        Args:
            types: a set of types
        """
        if not isinstance(types, Iterable):
            raise ValueError("types should be iterable")

        self.relation_graph, self.base_graph = build_graph(
            set(types) | {visions_generic}
        )
        self.types = set(self.relation_graph.nodes)

    def detect_series_type(self, series: pd.Series) -> Type[VisionsBaseType]:
        """Get the series type (without casting).

        Args:
            series: the Series to detect the type of

        Returns:
            The visions data type
        """
        base_type = traverse_graph(series, self.base_graph)
        return base_type

    def detect_frame_type(self, df: pd.DataFrame) -> Dict[str, Type[VisionsBaseType]]:
        """Detect the types of the series in the DataFrame, simple wrapper around get_series type.

        Args:
            df: the DataFrame to detect the types of

        Returns:
            A dict with the column names and visions data types
        """
        return {col: self.detect_series_type(df[col]) for col in df.columns}

    def infer_series_type(self, series: pd.Series) -> Type[VisionsBaseType]:
        """Infer the series type (without casting).

        Args:
            series: the Series to infer the type of

        Returns:
            The visions data type
        """
        inferred_path, _ = traverse_graph_inference(
            visions_generic, series, self.relation_graph
        )
        return inferred_path[-1]

    def infer_frame_type(self, df: pd.DataFrame) -> Dict[str, Type[VisionsBaseType]]:
        """Infer the types of the series in the DataFrame, simple wrapper around get_series type.

        Args:
            df: the DataFrame to infer the types of

        Returns:
            A dict with the column names and visions data types
        """
        return {col: self.infer_series_type(df[col]) for col in df.columns}

    def cast_series(self, series: pd.Series) -> pd.Series:
        """Cast Series to its inferred type.

        Args:
            series: the Series to cast

        Returns:
            A cast copy of the Series
        """

        series_type = self.detect_series_type(series)
        _, new_series = traverse_graph_inference(
            series_type, series, self.relation_graph
        )
        return new_series

    def cast_frame(self, df: pd.DataFrame) -> pd.DataFrame:
        """Cast to DataFrame, simple wrapper around cast_series.

        Args:
            df: the DataFrame to cast

        Returns:
            A copy of the DataFrame with cast
        """
        return pd.DataFrame({col: self.cast_series(df[col]) for col in df.columns})

    def cast_and_infer_series(self, series: pd.Series) -> pd.Series:
        """Cast Series to its inferred type.

        Args:
            series: the Series to cast

        Returns:
            A cast copy of the Series
        """

        series_type = self.detect_series_type(series)
        path, new_series = traverse_graph_inference(
            series_type, series, self.relation_graph
        )
        return path[-1], new_series

    def cast_and_infer_frame(self, df: pd.DataFrame) -> pd.DataFrame:
        """Cast to DataFrame, simple wrapper around cast_series.

        Args:
            df: the DataFrame to cast

        Returns:
            A copy of the DataFrame with cast
        """
        inferred_values = {col: self.cast_series(df[col]) for col in df.columns}
        inferred_types = {
            col: inf_type for col, (inf_type, _) in inferred_values.items()
        }
        inferred_series = {
            col: inf_series for col, (_, inf_series) in inferred_values.items()
        }
        return pd.DataFrame(inferred_series), inferred_types

    def output_graph(self, file_name: str, base_only: bool = False) -> None:
        """Write the type graph to a file.

        Args:
            file_name: the file to save the output to
            base_only: if True, plot the graph without relation mapping edges

        """

        if base_only:
            graph = self.base_graph.copy()
        else:
            graph = self.relation_graph.copy()

        graph.graph["node"] = {"shape": "box", "color": "red"}

        output_graph(graph, file_name)

    def plot_graph(self, dpi: int = 800):
        """

        Args:
            dpi: dpi of the matplotlib figure

        Returns:
            Shows the image
        """
        import matplotlib.pyplot as plt
        import matplotlib.image as mpimg
        import tempfile

        with tempfile.NamedTemporaryFile(suffix=".png") as temp_file:
            self.output_graph(temp_file.name)
            img = mpimg.imread(temp_file.name)
            plt.figure(dpi=dpi)
            plt.imshow(img)

    def _get_other_type(self, other):
        if issubclass(other.__class__, VisionsTypeset):
            other_types = set(other.types)
        elif issubclass(other, VisionsBaseType):
            other_types = {other}
        else:
            raise NotImplementedError(
                f"Typeset operation not implemented for type {type(other)}"
            )
        return other_types

    def __add__(self, other):
        other_types = self._get_other_type(other)
        return VisionsTypeset(self.types | other_types)

    def __sub__(self, other):
        other_types = self._get_other_type(other)
        return VisionsTypeset(self.types - other_types)

    def __repr__(self):
        return self.__class__.__name__

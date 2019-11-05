import warnings
from typing import Type, Tuple, List, Iterable

import pandas as pd
import networkx as nx

from visions.core.model.model_relation import model_relation
from visions.core.model.type import VisionsBaseType
from visions.utils.graph import output_graph
from visions.core.model.visions_generic import visions_generic


def build_relation_graph(nodes: set, relations: dict) -> Tuple[nx.DiGraph, nx.DiGraph]:
    """Constructs a traversable relation graph between visions types
    Builds a type relation graph from a collection of root and derivative nodes. Usually
    root nodes correspond to the baseline numpy types found in pandas while derivative
    nodes correspond to subtypes with a defined relation.
    Args:
        nodes:  A list of vision_types considered at the root of the relations graph.
        relations: A list of relations from type to types
    Returns:
        A directed graph of type relations for the provided nodes.
    """
    style_map = {True: "dashed", False: "solid"}
    relation_graph = nx.DiGraph()
    relation_graph.add_nodes_from(nodes)

    noninferential_edges = []

    for model, relation in relations.items():
        for friend_model, config in relation.items():
            if friend_model not in nodes:
                warnings.warn(
                    f"Provided relations included mapping from {friend_model} to {model} but {friend_model} was not included in the provided list of nodes"
                )
                continue
            relation_graph.add_edge(
                friend_model,
                model,
                relationship=model_relation(model, friend_model, **config._asdict()),
                style=style_map[config.inferential],
            )

            if not config.inferential:
                noninferential_edges.append((friend_model, model))

    check_graph_constraints(relation_graph, nodes)
    return relation_graph, relation_graph.edge_subgraph(noninferential_edges)


def check_graph_constraints(relation_graph: nx.DiGraph, nodes: set) -> None:
    """Validates a relation_graph is appropriately constructed
    Args:
        relation_graph: A directed graph representing the set of relations between type nodes.
        nodes:  A list of visions_types
        relations: A list of relations from type to types
    Returns:
        None
    """
    relation_graph.remove_nodes_from(list(nx.isolates(relation_graph)))

    orphaned_nodes = nodes - set(relation_graph.nodes)
    if orphaned_nodes:
        warnings.warn(
            f"{orphaned_nodes} were isolates in the type relation map and consequently\
                      orphaned. Please add some mapping to the orphaned nodes."
        )

    cycles = list(nx.simple_cycles(relation_graph))
    if len(cycles) > 0:
        warnings.warn(f"Cyclical relations between types {cycles} detected")


def traverse_relation_graph(
    series: pd.Series, G: nx.DiGraph, node: Type[VisionsBaseType] = visions_generic
) -> Type[VisionsBaseType]:
    """Depth First Search traversal. There should be at most one successor that contains the series.
    Args:
        series: the Series to check
        G: the Graph to traverse
        node: the current node
    Returns:
        The most uniquely specified node matching the series.
    """
    for vision_type in G.successors(node):
        if series in vision_type:
            return traverse_relation_graph(series, G, vision_type)

    return node


# Infer type with conversion
def get_type_inference_path(
    base_type: Type[VisionsBaseType], series: pd.Series, G: nx.DiGraph, path=None
) -> Tuple[List[Type[VisionsBaseType]], pd.Series]:
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

    for vision_type in G.successors(base_type):
        if G[base_type][vision_type]["relationship"].is_relation(series):
            new_series = G[base_type][vision_type]["relationship"].transform(series)
            return get_type_inference_path(vision_type, new_series, G, path)
    return path, series


def cast_along_path(series: pd.Series, path: List, G: nx.DiGraph):
    from_type = to_type = path[0]
    for to_type in path[1:]:
        new_series = G[from_type][to_type]["relationship"].transform(series)
    return new_series


def infer_type_path(
    series: pd.Series,
    G: nx.DiGraph,
    base_type: Type[VisionsBaseType] = visions_generic,
    sample_size: int = 10,
) -> Tuple[List[Type[VisionsBaseType]], pd.Series]:

    if sample_size >= len(series):
        path, new_series = get_type_inference_path(base_type, series, G)
        return path, new_series

    subseries = series.sample(sample_size)
    path, new_series = get_type_inference_path(base_type, subseries, G)

    from_type = to_type = path[0]
    for to_type in path[1:]:
        try:
            new_series = G[from_type][to_type]["relationship"].transform(series)
            from_type = to_type
        except Exception:
            break
    return path[0 : (path.index(to_type) + 1)], new_series


def cast_series_to_inferred_type(
    base_type: Type[VisionsBaseType], series: pd.Series, G: nx.DiGraph
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


class VisionsTypeset(object):
    """
    A collection of vision_types with an associated relationship map between them.
    Attributes:
        types: The collection of vision types which are derived either from a base_type or themselves
        relation_graph: ...
    """

    # TODO: Can we indicate covariance of types such that it's an Iterable[VisionsBaseType]
    def __init__(self, types: Iterable, build=True):
        """
        Args:
            types:
        """
        # self.column_type_map = {}

        self.relations = {}
        for node in set(types):
            self.relations[node] = node.get_relations()
        self._types = types
        if build:
            self._build_graph()

    def _build_graph(self):
        self.relation_graph, self.base_graph = build_relation_graph(
            self._types | {visions_generic}, self.relations
        )
        self.types = set(self.relation_graph.nodes)

    def get_series_type(self, series: pd.Series) -> Type[VisionsBaseType]:

        base_type = traverse_relation_graph(series, self.base_graph)
        return base_type

    def infer_series_type(self, series: pd.Series) -> Type[VisionsBaseType]:
        inferred_base_type, _ = infer_type_path(series, self.relation_graph)
        return inferred_base_type[-1]

    def cast_series(self, series: pd.Series) -> pd.Series:
        """
        Args:
            series:
        Returns:
        """
        series_type = self.get_series_type(series)
        return cast_series_to_inferred_type(series_type, series, self.relation_graph)

    def cast_to_inferred_types(self, df: pd.DataFrame) -> pd.DataFrame:
        return pd.DataFrame({col: self.cast_series(df[col]) for col in df.columns})

    def output_graph(self, file_name: str) -> None:
        """
        Args:
            file_name:
        Returns:
        """
        G = self.relation_graph.copy()
        G.graph["node"] = {"shape": "box", "color": "red"}

        output_graph(G, file_name)

    def plot_graph(self, dpi: int = 800):
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
            self.output_graph(temp_file.name)
            img = mpimg.imread(temp_file.name)
            plt.figure(dpi=dpi)
            plt.imshow(img)

    def __add__(self, other):
        # TODO: adding iterables of types?
        if issubclass(other.__class__, VisionsTypeset):
            other_types = set(other.types)
        elif issubclass(other, VisionsBaseType):
            other_types = {other}
        else:
            raise NotImplementedError(
                f"Typeset addition not implemented for type {type(other)}"
            )
        return VisionsTypeset(self.types | other_types)

    def __sub__(self, other):
        if issubclass(other.__class__, VisionsTypeset):
            other_types = set(other.types)
        elif issubclass(other, VisionsBaseType):
            other_types = {other}
        else:
            raise NotImplementedError(
                f"Typeset subtraction not implemented for type {type(other)}"
            )

        return VisionsTypeset(self.types - other_types)

    def __repr__(self):
        return self.__class__.__name__

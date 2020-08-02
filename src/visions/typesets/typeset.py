import warnings
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple, Type, Union, Any, Set
from functools import singledispatch

import networkx as nx
import pandas as pd

from visions.types.generic import Generic
from visions.types.type import VisionsBaseType


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

    style_map = {True: "dashed", False: "solid"}
    relation_graph = nx.DiGraph()
    relation_graph.add_nodes_from(nodes)

    noninferential_edges = []

    for node in nodes:
        for relation in node.get_relations():
            if relation.related_type not in nodes:
                warnings.warn(
                    "Provided relations included mapping from {related_type} to {own_type} but {related_type} was not included in the provided list of nodes".format(
                        related_type=relation.related_type, own_type=relation.type
                    )
                )
            else:
                relation_graph.add_edge(
                    relation.related_type,
                    relation.type,
                    relationship=relation,
                    style=style_map[relation.inferential],
                )

                if not relation.inferential:
                    noninferential_edges.append((relation.related_type, relation.type))

    check_graph_constraints(relation_graph)

    base_graph = relation_graph.edge_subgraph(noninferential_edges)
    return relation_graph, base_graph


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
    root_node = next(nx.topological_sort(graph))

    isolates = list(set(nx.isolates(graph)) - {root_node})  # root can be isolate
    graph.remove_nodes_from(isolates)
    orphaned_nodes = nodes - set(graph.nodes)
    if orphaned_nodes:
        message = f"{orphaned_nodes} were isolates in the type relation map and consequently orphaned. "
        message += "Please add some mapping to the orphaned nodes."
        warnings.warn(message)


def check_cycles(graph: nx.DiGraph) -> None:
    """Check for cycles and warn if one is found

    Args:
        graph: the graph to check

    """
    cycles = list(nx.simple_cycles(graph))
    if len(cycles) > 0:
        warnings.warn(
            "Cyclical relations between types {cycles} detected".format(cycles=cycles)
        )


def traverse_graph_with_series(
    base_type: Type[VisionsBaseType],
    series: pd.Series,
    graph: nx.DiGraph,
    path: List[Type[VisionsBaseType]] = None,
) -> Tuple[pd.Series, List[Type[VisionsBaseType]]]:
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

    path.append(base_type)

    for vision_type in graph.successors(base_type):
        relation = graph[base_type][vision_type]["relationship"]
        if relation.is_relation(series):
            series = relation.transform(series)
            return traverse_graph_with_series(vision_type, series, graph, path)

    return series, path


def traverse_graph_with_sampled_series(
    base_type: Type[VisionsBaseType],
    series: pd.Series,
    graph: nx.DiGraph,
    sample_size: int = 10,
) -> Tuple[pd.Series, List[Type[VisionsBaseType]]]:
    """Depth First Search traversal with sampling. There should be at most one successor that contains the series.

    Args:
        series: the Series to check
        graph: the Graph to traverse
        node: the current node
        path: the path so far

    Returns:
        The most uniquely specified node matching the series.
    """

    if (series.shape[0] < 1000) or (sample_size > series.shape[0]):
        return traverse_graph_with_series(base_type, series, graph)

    series_sample = series.sample(sample_size)
    _, path = traverse_graph_with_series(base_type, series_sample, graph)
    if len(path) == 1:
        return series, path

    # Cast the full series
    from_type = path[0]
    for i, to_type in enumerate(path[1:]):
        relation = graph[from_type][to_type]["relationship"]
        if not relation.is_relation(series):
            break
        series = relation.transform(series)
        from_type = to_type

    return series, path[0 : (i + 2)]


@singledispatch
def traverse_graph(
    data: Any, root_node: Type[VisionsBaseType], graph: nx.DiGraph
) -> Tuple[Any, Any]:
    raise TypeError(f"Undefined graph traversal over data of type {type(data)}")


@traverse_graph.register
def _(
    series: pd.Series, root_node: Type[VisionsBaseType], graph: nx.DiGraph
) -> Tuple[pd.Series, List[Type[VisionsBaseType]]]:
    return traverse_graph_with_series(root_node, series, graph)


@traverse_graph.register
def _(
    df: pd.DataFrame, root_node: Type[VisionsBaseType], graph: nx.DiGraph
) -> Tuple[pd.DataFrame, Dict[str, List[Type[VisionsBaseType]]]]:
    inferred_values = {
        col: traverse_graph(df[col], root_node, graph) for col in df.columns
    }
    inferred_paths = {col: inf_path for col, (_, inf_path) in inferred_values.items()}
    inferred_series = {
        col: inf_series for col, (inf_series, _) in inferred_values.items()
    }
    return pd.DataFrame(inferred_series), inferred_paths


@singledispatch
def get_type_from_path(path_data: Any) -> Any:
    raise TypeError(f"Can't get types from path object of type {type(path_data)}")


@get_type_from_path.register
def _(path_dict: dict) -> Dict[str, Type[VisionsBaseType]]:
    return {k: get_type_from_path(v) for k, v in path_dict.items()}


@get_type_from_path.register
def _(path_list: List[Type[VisionsBaseType]]) -> Type[VisionsBaseType]:
    return path_list[-1]


@get_type_from_path.register
def _(path_list: Tuple[Type[VisionsBaseType]]) -> Type[VisionsBaseType]:
    return path_list[-1]


class VisionsTypeset(object):
    """
    A set of visions types with an associated relationship map between them.

    Attributes:
        types: The collection of vision types which are derived either from a base_type or themselves
        base_graph: the graph with relations to parent types
        relation_graph: the graph with relations to the parent types and mapping relations
    """

    def __init__(self, types: Set[Type[VisionsBaseType]]) -> None:
        """
        Args:
            types: a set of types
        """
        self._root_node = None

        if not isinstance(types, Iterable):
            raise ValueError("types should be iterable")

        self.relation_graph, self.base_graph = build_graph(set(types))

        if not issubclass(self.root_node, Generic):
            raise ValueError("`root_node` should be a subclass of Generic")

        self.types = set(self.relation_graph.nodes)

    @property
    def root_node(self) -> Type[VisionsBaseType]:
        """Returns a cached copy of the relation_graphs root node
        
        Args:

        Returns:
            A cached copy of the relation_graphs root node.
        """
        if self._root_node is None:
            self._root_node = next(nx.topological_sort(self.relation_graph))
        return self._root_node

    def detect_type(
        self, data: Union[pd.DataFrame, pd.Series]
    ) -> Type[VisionsBaseType]:
        """The inferred type found only considering IdentityRelations.

        Args:
            data: a DataFrame or Series to determine types over

        Returns:
            A dictionary of {name: type} pairs in the case of DataFrame input or a type
        """
        _, paths = traverse_graph(data, self.root_node, self.base_graph)
        return get_type_from_path(paths)

    def infer_type(self, data: Union[pd.DataFrame, pd.Series]) -> Type[VisionsBaseType]:
        """The inferred type found using all type relations.

        Args:
            data: a DataFrame or Series to determine types over

        Returns:
            A dictionary of {name: type} pairs in the case of DataFrame input or a type
        """
        _, paths = traverse_graph(data, self.root_node, self.relation_graph)
        return get_type_from_path(paths)

    def cast(
        self, data: Union[pd.DataFrame, pd.Series]
    ) -> Union[pd.DataFrame, pd.Series]:
        """Transforms input data into a canonical representation using only IdentityRelations

        Args:
            data: a DataFrame or Series to determine types over

        Returns:
            new_data: The transformed DataFrame or Series.
        """
        data, _ = traverse_graph(data, self.root_node, self.base_graph)
        return data

    def infer_and_cast(
        self, data: Union[pd.DataFrame, pd.Series]
    ) -> Tuple[Union[pd.DataFrame, pd.Series], Any]:
        """Transforms input data and returns it's corresponding new type relation using all relations.
        Args:
            data: a DataFrame or Series to determine types over

        Returns:
            new_data: The transformed DataFrame or Series.
            types: A dictionary of {name: type} pairs in the case of DataFrame input or a type.
        """
        data, paths = traverse_graph(data, self.root_node, self.relation_graph)
        return data, get_type_from_path(paths)

    def output_graph(
        self,
        file_name: Union[str, Path],
        base_only: bool = False,
        dpi: Optional[int] = None,
    ) -> None:
        """Write the type graph to a file.

        Args:
            file_name: the file to save the output to
            base_only: if True, plot the graph without relation mapping edges
            dpi: set the dpi of the output image
        """
        from visions.utils.graph import output_graph

        if base_only:
            graph = self.base_graph.copy()
        else:
            graph = self.relation_graph.copy()

        graph.graph["node"] = {"shape": "box", "color": "red"}
        if dpi is not None:
            graph.graph["graph"] = {"dpi": dpi}

        output_graph(graph, file_name)

    def plot_graph(self, dpi: int = 800, base_only: bool = False):
        """

        Args:
            dpi: dpi of the matplotlib figure.
            base_only: Only plot the type graph corresponding to IdentityRelations.
        Returns:
            Displays the image
        """
        import tempfile
        import os

        from matplotlib import image as mpimg
        from matplotlib import pyplot as plt

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp_file:
            self.output_graph(temp_file.name, dpi=dpi, base_only=base_only)
            img = mpimg.imread(temp_file.name)
            plt.figure(dpi=dpi)
            plt.axis("off")
            plt.imshow(img)
        os.unlink(temp_file.name)

    def _get_other_type(
        self, other: Union[Type[VisionsBaseType], "VisionsTypeset"]
    ) -> Set[Type[VisionsBaseType]]:
        if issubclass(other.__class__, VisionsTypeset):
            other_types = set(other.types)
        elif issubclass(other, VisionsBaseType):
            other_types = {other}
        else:
            raise NotImplementedError(
                "Typeset operation not implemented for type {other_type}".format(
                    other_type=type(other)
                )
            )
        return other_types

    def replace(
        self, old: Type[VisionsBaseType], new: Type[VisionsBaseType]
    ) -> "VisionsTypeset":
        """Create a new typeset having replace one type with another.

        Args:
            old: Type to replace.
            new: Replacement type.
        
        Returns
            A VisionsTypeset
        """
        types = self.types.copy()
        types.add(new)
        types.remove(old)
        return VisionsTypeset(types)

    def __add__(
        self, other: Union[Type[VisionsBaseType], "VisionsTypeset"]
    ) -> "VisionsTypeset":
        """Adds a type or typeset into the current typeset.

        Args:
            other: Type or typeset to be added
        
        Returns
            A VisionsTypeset
        """
        other_types = self._get_other_type(other)
        return VisionsTypeset(self.types | other_types)

    def __iadd__(
        self, other: Union[Type[VisionsBaseType], "VisionsTypeset"]
    ) -> "VisionsTypeset":
        """Adds a type or typeset into the current typeset.

        Args:
            other: Type or typeset to be added
        
        Returns
            A VisionsTypeset
        """
        return self.__add__(other)

    def __sub__(
        self, other: Union[Type[VisionsBaseType], "VisionsTypeset"]
    ) -> "VisionsTypeset":
        """Subtracts a type or typeset from the current typeset.

        Args:
            other: Type or typeset to be removed
        
        Returns
            A VisionsTypeset
        """
        other_types = self._get_other_type(other)
        return VisionsTypeset(self.types - other_types)

    def __isub__(
        self, other: Union[Type[VisionsBaseType], "VisionsTypeset"]
    ) -> "VisionsTypeset":
        """Subtracts a type or typeset from the current typeset.

        Args:
            other: Type or typeset to be removed
        
        Returns
            A VisionsTypeset
        """
        return self.__sub__(other)

    def __repr__(self) -> str:
        """Pretty representation of the typeset.
        
        Returns
            A VisionsTypeset
        """
        return self.__class__.__name__

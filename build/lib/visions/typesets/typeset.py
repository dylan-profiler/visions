import warnings
from functools import singledispatch
from pathlib import Path
from typing import (
    Any,
    Dict,
    Iterable,
    List,
    Optional,
    Sequence,
    Set,
    Tuple,
    Type,
    TypeVar,
    Union,
)

import networkx as nx
import pandas as pd

from visions.types.generic import Generic
from visions.types.type import VisionsBaseType

TypeOrTypeset = TypeVar("TypeOrTypeset", Type[VisionsBaseType], "VisionsTypeset")
pathTypes = TypeVar(
    "pathTypes", Type[VisionsBaseType], Dict[str, Type[VisionsBaseType]]
)
pdT = TypeVar("pdT", pd.Series, pd.DataFrame)
T = Type[VisionsBaseType]


def build_graph(nodes: Set[Type[VisionsBaseType]]) -> Tuple[nx.DiGraph, nx.DiGraph]:
    """Constructs a traversable relation graph between visions types

    Builds a type relation graph from a collection of :class:`visions.types.type.VisionsBaseType` where
    each node corresponds to a type and each edge is a relation defined on the type.

    Args:
        nodes:  An Sequence of :class:`visions.types.type.VisionsBaseType`

    Returns:
        A directed graph of type relations for the provided nodes.
    """

    style_map = {True: "dashed", False: "solid"}
    relation_graph = nx.DiGraph()
    relation_graph.add_nodes_from(nodes)

    noninferential_edges = []

    for node in nodes:
        for relation in node.relations:
            if relation.related_type not in nodes:
                warnings.warn(
                    f"Provided relations included mapping from {relation.related_type} to {relation.type} "
                    f"but {relation.related_type} was not included in the provided list of nodes"
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
        warnings.warn(f"Cyclical relations between types {cycles} detected")


def traverse_graph_with_series(
    base_type: T,
    series: Sequence,
    graph: nx.DiGraph,
    path: List[T] = None,
    state: Optional[dict] = None,
) -> Tuple[Sequence, List[T], dict]:
    """Depth First Search traversal. There should be at most one successor that contains the series.

    Args:
        base_type: Entry-point for graph to start traversal
        series: the Series to check
        graph: the Graph to traverse
        path: the path so far
        state: traversal state

    Returns:
        The most uniquely specified node matching the series.
    """
    if state is None:
        state = dict()

    if path is None:
        path = []

    path.append(base_type)

    for vision_type in graph.successors(base_type):
        relation = graph[base_type][vision_type]["relationship"]
        if relation.is_relation(series, state):
            series = relation.transform(series, state)
            return traverse_graph_with_series(vision_type, series, graph, path, state)

    return series, path, state


def traverse_graph_with_sampled_series(
    base_type: T,
    series: pd.Series,
    graph: nx.DiGraph,
    sample_size: int = 10,
    state: dict = dict(),
) -> Tuple[Sequence, List[T], dict]:
    """Depth First Search traversal with sampling. There should be at most one successor that contains the series.

    Args:
        base_type: Entry-point for graph to start  traversal
        series: the Series to check
        graph: the Graph to traverse
        sample_size: number of items used in heuristic traversal
        state: traversal state

    Returns:
        The most uniquely specified node matching the series.
    """

    if (series.shape[0] < 1000) or (sample_size > series.shape[0]):
        return traverse_graph_with_series(base_type, series, graph, state=state)

    series_sample = series.sample(sample_size)
    _, path, _ = traverse_graph_with_series(
        base_type, series_sample, graph, state=state
    )
    if len(path) == 1:
        return series, path, state

    # Cast the full series
    from_type = path[0]
    for i, to_type in enumerate(path[1:]):
        relation = graph[from_type][to_type]["relationship"]
        if not relation.is_relation(series, state):
            break
        series = relation.transform(series, state)
        from_type = to_type

    return series, path[0 : (i + 2)], state


@singledispatch
def traverse_graph(
    data: Sequence, root_node: T, graph: nx.DiGraph
) -> Tuple[Sequence, Union[List[T], Dict[str, List[T]]], Dict[str, dict]]:
    return traverse_graph_with_series(root_node, data, graph)


@singledispatch
def get_type_from_path(
    path_data: Union[Sequence[T], Dict[str, Sequence[T]]]
) -> Union[T, Dict[str, T]]:
    raise TypeError(f"Can't get types from path object of type {type(path_data)}")


@get_type_from_path.register(list)
@get_type_from_path.register(tuple)
def _get_type_from_path_builtin(path_list: Sequence[T]) -> T:
    return path_list[-1]


@get_type_from_path.register(dict)
def _get_type_from_path_dict(path_dict: Dict[str, Sequence[T]]) -> Dict[str, T]:
    return {k: v[-1] for k, v in path_dict.items()}


class VisionsTypeset:
    """
    A collection of :class:`visions.types.type.VisionsBaseType` with  associated relationship map between them.

    Attributes:
        types: The collection of Visions Types derived from :class:`visions.types.type.VisionsBaseType`
        base_graph: The graph of relations composed exclusively of :class:`visions.relations.relations.IdentityRelation`
        relation_graph: The full relation graph including both :class:`visions.relations.relations.IdentityRelation`
            and :class:`visions.relations.relations.InferenceRelation`
    """

    def __init__(self, types: Set[Type[VisionsBaseType]]) -> None:
        """
        Args:
            types: a set of types
        """
        self._root_node: Optional[T] = None

        if not isinstance(types, Iterable):
            raise ValueError("types should be Sequence")

        self.relation_graph, self.base_graph = build_graph(set(types))

        if not issubclass(self.root_node, Generic):
            raise ValueError("`root_node` should be a subclass of Generic")

        self.types = set(self.relation_graph.nodes)

    @property
    def root_node(self) -> T:
        """Returns a cached copy of the relation_graphs root node

        Args:

        Returns:
            A cached copy of the relation_graphs root node.
        """
        if self._root_node is None:
            self._root_node = next(nx.topological_sort(self.relation_graph))
        return self._root_node

    def detect(self, data: Any) -> Tuple[Sequence, Any, dict]:
        """The results found after only considering IdentityRelations.

        Notes:
            This is an advanced feature, consider using `detect_type` in case the type is what is needed.

        Args:
            data: a DataFrame or Series to determine types over

        Returns:
            A tuple of the coerced sequence, visited nodes and state
        """
        return traverse_graph(data, self.root_node, self.base_graph)

    def detect_type(self, data: Sequence) -> Union[T, Dict[str, T]]:
        """The inferred type found only considering IdentityRelations.

        Args:
            data: a DataFrame or Series to determine types over

        Returns:
            A dictionary of {name: type} pairs in the case of DataFrame input or a type
        """
        _, paths, _ = self.detect(data)
        return get_type_from_path(paths)

    def infer(self, data: Sequence) -> Tuple[Sequence, Any, dict]:
        """The results found after considering all relations.

        Notes:
            This is an advanced feature, consider using `infer_type` in case the type is what is needed.

        Args:
            data: a DataFrame or Series to determine types over

        Returns:
            A tuple of the coerced sequence, visited nodes and state
        """
        return traverse_graph(data, self.root_node, self.relation_graph)

    def infer_type(self, data: Sequence) -> Union[T, Dict[str, T]]:

        """The inferred type found using all type relations.

        Args:
            data: a DataFrame or Series to determine types over

        Returns:
            A dictionary of {name: type} pairs in the case of DataFrame input or a type
        """
        _, paths, _ = self.infer(data)
        return get_type_from_path(paths)

    def cast_to_detected(self, data: Sequence) -> Sequence:
        """Transforms input data into a canonical representation using only IdentityRelations

        Args:
            data: a DataFrame or Series to determine types over

        Returns:
            new_data: The transformed DataFrame or Series.
        """
        data, _, _ = self.detect(data)
        return data

    def cast_to_inferred(self, data: Sequence) -> Sequence:
        """Transforms input data and returns it's corresponding new type relation using all relations.

        Args:
            data: a DataFrame or Series to determine types over

        Returns:
            new_data: The transformed DataFrame or Series.
            types: A dictionary of {name: type} pairs in the case of DataFrame input or a type.
        """
        data, _, _ = self.infer(data)
        return data

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

    def plot_graph(
        self,
        dpi: int = 800,
        base_only: bool = False,
        figsize: Optional[Tuple[int, int]] = None,
    ):
        """

        Args:
            dpi: dpi of the matplotlib figure.
            figsize: figure size
            base_only: Only display the typesets base_graph
        Returns:
            Displays the image
        """
        import os
        import tempfile

        from matplotlib import image as mpimg
        from matplotlib import pyplot as plt

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp_file:
            self.output_graph(temp_file.name, dpi=dpi, base_only=base_only)
            img = mpimg.imread(temp_file.name)
            plt.figure(dpi=dpi, figsize=figsize)
            plt.axis("off")
            plt.imshow(img)
        os.unlink(temp_file.name)

    def _get_other_type(self, other: TypeOrTypeset) -> Set[T]:
        """Converts input into a set of :class:`visions.types.type.VisionsBaseType`

        Args:
            other: A :class:`visions.types.type.VisionsBaseType` or :class:`visions.typesets.typeset.VisionsTypeset`

        Raises:
            NotImplementedError:

        Returns:
            Set[Type[VisionsBaseType]]:
        """
        if isinstance(other, VisionsTypeset):
            other_types = set(other.types)
        elif issubclass(other, VisionsBaseType):
            other_types = {other}
        else:
            raise NotImplementedError(
                f"Typeset operation not implemented for type {type(other)}"
            )
        return other_types

    def replace(self, old: T, new: T) -> "VisionsTypeset":
        """Create a new typeset having replace one type with another.

        Args:
            old: Visions type to replace.
            new: Replacement visions type.

        Returns
            A VisionsTypeset
        """
        types = self.types.copy()
        types.add(new)
        types.remove(old)
        return VisionsTypeset(types)

    def __add__(self, other: TypeOrTypeset) -> "VisionsTypeset":
        """Adds a type or typeset into the current typeset.

        Args:
            other: Type or typeset to be added

        Returns
            A VisionsTypeset
        """
        other_types = self._get_other_type(other)
        return VisionsTypeset(self.types | other_types)

    def __iadd__(self, other: TypeOrTypeset) -> "VisionsTypeset":
        """Adds a type or typeset into the current typeset.

        Args:
            other: Type or typeset to be added

        Returns
            A VisionsTypeset
        """
        return self.__add__(other)

    def __sub__(self, other: TypeOrTypeset) -> "VisionsTypeset":
        """Subtracts a type or typeset from the current typeset.

        Args:
            other: Type or typeset to be removed

        Returns
            A VisionsTypeset
        """
        other_types = self._get_other_type(other)
        return VisionsTypeset(self.types - other_types)

    def __isub__(self, other: TypeOrTypeset) -> "VisionsTypeset":
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
            A :class:`visions.typesets.typeset.VisionsTypeset`
        """
        return self.__class__.__name__

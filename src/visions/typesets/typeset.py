import warnings
from functools import singledispatch
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Set, Tuple, Type, TypeVar, Union

import networkx as nx
import pandas as pd

from visions.types.generic import Generic
from visions.types.type import VisionsBaseType

pdT = TypeVar("pdT", pd.Series, pd.DataFrame)
TypeOrTypeset = TypeVar("TypeOrTypeset", Type[VisionsBaseType], "VisionsTypeset")
pathTypes = TypeVar(
    "pathTypes", Type[VisionsBaseType], Dict[str, Type[VisionsBaseType]]
)


def build_graph(nodes: Set[Type[VisionsBaseType]]) -> Tuple[nx.DiGraph, nx.DiGraph]:
    """Constructs a traversable relation graph between visions types

    Builds a type relation graph from a collection of :class:`visions.types.type.VisionsBaseType` where
    each node corresponds to a type and each edge is a relation defined on the type.

    Args:
        nodes:  An iterable of :class:`visions.types.type.VisionsBaseType`

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
        base_type: Entry-point for graph to start traversal
        series: the Series to check
        graph: the Graph to traverse
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
        base_type: Entry-point for graph to start  traversal
        series: the Series to check
        graph: the Graph to traverse
        sample_size: number of items used in heuristic traversal

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
    data: pdT, root_node: Type[VisionsBaseType], graph: nx.DiGraph
) -> Tuple[pdT, Any]:
    raise TypeError(f"Undefined graph traversal over data of type {type(data)}")


@traverse_graph.register(pd.Series)
def _(
    series: pd.Series, root_node: Type[VisionsBaseType], graph: nx.DiGraph
) -> Tuple[pd.Series, List[Type[VisionsBaseType]]]:
    return traverse_graph_with_series(root_node, series, graph)


@traverse_graph.register(pd.DataFrame)  # type: ignore
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
def get_type_from_path(path_data: Any) -> pathTypes:
    raise TypeError(f"Can't get types from path object of type {type(path_data)}")


@get_type_from_path.register(dict)  # type: ignore
def _(path_dict: dict) -> Dict[str, Type[VisionsBaseType]]:
    return {k: get_type_from_path(v) for k, v in path_dict.items()}


@get_type_from_path.register(list)  # type: ignore
def _(path_list: list) -> Type[VisionsBaseType]:
    return path_list[-1]


@get_type_from_path.register(tuple)  # type: ignore
def _(path_list: tuple) -> Type[VisionsBaseType]:
    return path_list[-1]


class VisionsTypeset(object):
    """
    A collection of :class:`visions.types.type.VisionsBaseType` with  associated relationship map between them.

    Attributes:
        types: The collection of Visions Types derived from :class:`visions.types.type.VisionsBaseType`
        base_graph: The graph of relations composed exclusively of :class:`visions.relations.relations.IdentityRelation`
        relation_graph: The full relation graph including both :class:`visions.relations.relations.IdentityRelation` and :class:`visions.relations.relations.InferenceRelation`
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
        return self._root_node  # type: ignore

    @staticmethod
    def _traverse_graph(data: pdT, root_node, graph):
        return traverse_graph(data, root_node, graph)

    def detect_type(self, data: pdT) -> pathTypes:
        """The inferred type found only considering IdentityRelations.

        Args:
            data: a DataFrame or Series to determine types over

        Returns:
            A dictionary of {name: type} pairs in the case of DataFrame input or a type
        """
        _, paths = self._traverse_graph(data, self.root_node, self.base_graph)
        return get_type_from_path(paths)

    def infer_type(self, data: pdT) -> pathTypes:
        """The inferred type found using all type relations.

        Args:
            data: a DataFrame or Series to determine types over

        Returns:
            A dictionary of {name: type} pairs in the case of DataFrame input or a type
        """
        _, paths = self._traverse_graph(data, self.root_node, self.relation_graph)
        return get_type_from_path(paths)

    def cast_to_detected(self, data: pdT) -> pdT:
        """Transforms input data into a canonical representation using only IdentityRelations

        Args:
            data: a DataFrame or Series to determine types over

        Returns:
            new_data: The transformed DataFrame or Series.
        """
        data, _ = self._traverse_graph(data, self.root_node, self.base_graph)
        return data

    def cast_to_inferred(self, data: pdT) -> Tuple[pdT, pathTypes]:
        """Transforms input data and returns it's corresponding new type relation using all relations.

        Args:
            data: a DataFrame or Series to determine types over

        Returns:
            new_data: The transformed DataFrame or Series.
            types: A dictionary of {name: type} pairs in the case of DataFrame input or a type.
        """
        data, _ = self._traverse_graph(data, self.root_node, self.relation_graph)
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

    def plot_graph(self, dpi: int = 800, base_only: bool = False):
        """

        Args:
            dpi: dpi of the matplotlib figure.
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
            plt.figure(dpi=dpi)
            plt.axis("off")
            plt.imshow(img)
        os.unlink(temp_file.name)

    def _get_other_type(self, other: TypeOrTypeset) -> Set[Type[VisionsBaseType]]:
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
                "Typeset operation not implemented for type {other_type}".format(
                    other_type=type(other)
                )
            )
        return other_types

    def replace(self, old: VisionsBaseType, new: VisionsBaseType) -> "VisionsTypeset":
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

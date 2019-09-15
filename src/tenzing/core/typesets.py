import pandas as pd
import networkx as nx
from networkx.drawing.nx_agraph import write_dot
from tenzing.core.model_implementations.types.tenzing_generic import tenzing_generic


def build_relation_graph(nodes):
    """Constructs a traversible relation graph between tenzing types
    Builds a type relation graph from a collection of root and derivative nodes. Usually
    root nodes correspond to the baseline numpy types found in pandas while derivative
    nodes correspond to subtypes with a defined relation.
    Parameters
    ----------
    root_nodes : List[tenzing_type]
        A list of tenzing_types considered at the root of the relations graph.
    derivative_nodes : List[tenzing_type]
        A list of tenzing_types with defined relations either to the root_nodes or each other.
    Returns
    -------
    networkx DiGraph
        A directed graph of type relations for the provided nodes.
    Notes
    -------
     So much duplicated code here... got to be a better way. The fundamental issue
        is that I have to modify the data to check the next step in the graph.
        I could re-use some of this code but then I end up double performing those
        cast operations
    """
    nodes = set(nodes) | {tenzing_generic}

    relation_graph = nx.DiGraph()
    relation_graph.add_nodes_from(nodes)
    relation_graph.add_edges_from(node.edge for s_node in nodes for to_node, node in s_node.get_relations().items())

    relations = {node.edge: {'relationship': node}
                 for s_node in nodes for to_node, node in s_node.get_relations().items()}
    nx.set_edge_attributes(relation_graph, relations)

    check_graph_constraints(relation_graph, nodes)
    return relation_graph


def check_graph_constraints(relation_graph, nodes):
    undefined_nodes = set(relation_graph.nodes) - nodes
    relation_graph.remove_nodes_from(undefined_nodes)
    relation_graph.remove_nodes_from(list(nx.isolates(relation_graph)))

    orphaned_nodes = [n for n in nodes if n not in set(relation_graph.nodes)]

    assert not orphaned_nodes, f'{orphaned_nodes} were isolates in the type relation map and consequently orphaned. Please add some mapping to the orphaned nodes.'
    cycles = list(nx.simple_cycles(relation_graph))
    assert len(cycles) == 0, f'Cyclical relations between types {cycles} detected'

    # TODO: this should be forced by framework...
    # Relations should be connected...
    # orphaned_nodes = [n for n in provided_nodes if n not in set(relation_graph.nodes)]
    # assert not orphaned_nodes, f'{orphaned_nodes} were isolates in the type relation map and consequently orphaned. Please add some mapping to the orphaned nodes.'


def traverse_relation_graph(series, G, node=tenzing_generic):
    """
    Depth-first search
    """
    for tenz_type in G.successors(node):
        if series in tenz_type:  # TODO: generalize check
            return traverse_relation_graph(series, G, tenz_type)
    return node


# TODO: merge two functions
def get_type_inference_path(base_type, series, G, path=None):
    if path is None:
        path = []
    path.append(base_type)
    for tenz_type in G.successors(base_type):
        if G[base_type][tenz_type]["relationship"].is_relation(series):
            # print("Transform", series.name, "from", base_type, "to", tenz_type)
            new_series = G[base_type][tenz_type]["relationship"].transform(series)
            return get_type_inference_path(tenz_type, new_series, G, path)
    return path


def cast_to_inferred_type(series, base_type, G):
    for tenz_type in G.successors(base_type):
        if G[base_type][tenz_type]["relationship"].is_relation(series):
            # print("Cast", series.name, "from", base_type, "to", tenz_type)
            new_series = G[base_type][tenz_type]["relationship"].transform(series)
            return cast_to_inferred_type(new_series, tenz_type, G)
    return series


def infer_type(base_type, series, G):
    path = get_type_inference_path(base_type, series, G)
    return path[-1]


class tenzingTypeset(object):
    """
    A collection of tenzing_types with an associated relationship map between them.

    Attributes
    ----------
    types: frozenset
        The collection of tenzing types which are derived either from a base_type or themselves
    """

    def __init__(self, types):
        """

        Parameters
        ----------
        types : List[tenzing_type]
            The collection of tenzing types at the root of the relations graph

        Returns
        -------
        self

        """
        # TODO: raise error if types miss parent
        self.types = frozenset(types)

        self.relation_graph = build_relation_graph(self.types)

        self.column_summary = {}

    """Base class for working with collections of tenzing types on a dataset

    A tenzingTypeset represents a collection of tenzingTypes

    Attributes
    ----------
    base_types : list
        The collection of tenzing types at the root of the relations graph. This will usually be
        basic pandas types like `int`, `float`, `object`, etc...

    derivative_types: list
        A List of tenzing types which are derived either from a base_type or themselves. For example,
        `tenzing_string` is represented by `object` in it's underlying pandas/numpy datatype.

    """

    def prep(self, df):
        # TODO: improve this (no new attributes outside of __init__)
        self.column_type_map = {
            col: self._get_column_type(df[col]) for col in df.columns
        }
        # self.is_prepped = True

    def summarize(self, df):
        # assert (
        #     self.is_prepped
        # ), "typeset hasn't been prepped for your dataset yet. Call .prep(df)"
        self.prep(df)
        summary = {
            col: self.column_type_map[col].summarize(df[col]) for col in df.columns
        }
        self.column_summary = summary
        return self.column_summary

    def general_summary(self, df):
        return {
            "n_observations": df.shape[0],
            "n_variables": df.shape[1],
            "memory_size": df.memory_usage(index=True, deep=True).sum(),
        }

    def summary_report(self, df):
        general_summary = self.general_summary(df)
        column_summary = self.summarize(df)
        return {
            "types": self.column_type_map,
            "columns": column_summary,
            "general": general_summary,
        }

    def infer_types(self, df):
        # Without prep, makes little sense
        self.prep(df)
        return {col: self.infer_series_type(df[col]) for col in df.columns}

    def cast_to_inferred_types(self, df):
        return pd.DataFrame(
            {col: self.cast_series_to_inferred_type(df[col]) for col in df.columns}
        )

    def infer_series_type(self, series):
        return infer_type(self.column_type_map[series.name],
                          series,
                          self.relation_graph)

    def cast_series_to_inferred_type(self, series):
        return cast_to_inferred_type(series,
                                     self.column_type_map[series.name],
                                     self.relation_graph)

    def _get_column_type(self, series):
        # walk the relation_map to determine which is most uniquely specified
        return traverse_relation_graph(series, self.relation_graph)

    def write_dot(self):
        G = self.relation_graph.copy()
        G.graph["node"] = {"shape": "box", "color": "red"}

        write_dot(G, "graph_relations.dot")

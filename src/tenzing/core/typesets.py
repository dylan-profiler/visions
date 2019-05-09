from tenzing.core.summary import summary_report
import pandas as pd
import networkx as nx
import itertools


def build_relation_graph(root_nodes, derivative_nodes):
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
    relation_graph = nx.DiGraph()
    relation_graph.add_node('root')
    relation_graph.add_nodes_from(root_nodes)
    relation_graph.add_edges_from(itertools.product(['root'], root_nodes))
    relation_graph.add_nodes_from(derivative_nodes)
    relation_graph.add_edges_from(node.edge for s_node in root_nodes for to_node, node in s_node.relations.items())
    relation_graph.add_edges_from(node.edge for s_node in derivative_nodes for to_node, node in s_node.relations.items())

    relations = {node.edge: {'relationship': node} for s_node in root_nodes for to_node, node in s_node.relations.items()}
    nx.set_edge_attributes(relation_graph, relations)

    relations = {node.edge: {'relationship': node} for s_node in derivative_nodes for to_node, node in s_node.relations.items()}
    nx.set_edge_attributes(relation_graph, relations)

    provided_nodes = set(root_nodes) | set(derivative_nodes)
    undefined_nodes = set(relation_graph.nodes) - (set(['root']) | provided_nodes)
    relation_graph.remove_nodes_from(undefined_nodes)
    relation_graph.remove_nodes_from(list(nx.isolates(relation_graph)))

    orphaned_nodes = [n for n in provided_nodes if n not in set(relation_graph.nodes)]

    assert not orphaned_nodes, f'{orphaned_nodes} were isolates in the type relation map and consequently orphaned. Please add some mapping to the orphaned nodes.'
    cycles = list(nx.simple_cycles(relation_graph))
    assert len(cycles) == 0, f'Cyclical relations between types {cycles} detected'
    return relation_graph


def traverse_relation_graph(series, G, node='root'):
    for tenz_type in G.successors(node):
        if series in tenz_type:
            return traverse_relation_graph(series, G, tenz_type)
    return node


def get_type_inference_path(base_type, series, G, path=[]):
    path.append(base_type)
    for tenz_type in G.successors(base_type):
        if G[base_type][tenz_type]['relationship'].is_relation(series):
            new_series = G[base_type][tenz_type]['relationship'].transform(series)
            return get_type_inference_path(tenz_type, new_series, G, path)
    return path


def infer_type(base_type, series, G):
    path = get_type_inference_path(base_type, series, G)
    return path[-1]


def cast_to_inferred_type(series, base_type, G):
    for tenz_type in G.successors(base_type):
        if G[base_type][tenz_type]['relationship'].is_relation(series):
            new_series = G[base_type][tenz_type]['relationship'].transform(series)
            return cast_to_inferred_type(new_series, tenz_type, G)
    return series


class tenzing_typeset:
    """
    A collection of tenzing_types with an associated relationship map between them.

    Attributes
    ----------
    base_types : frozenset
        The collection of tenzing types at the root of the relations graph

    derivative_types: frozenset
        The collection of tenzing types which are derived either from a base_type or themselves

    types: frozenset
        The collection of both base_types and derivative_types

    relation_map: networkx DiGraph
        A graph representing the relationships and mappings between each type in the typeset.

    """
    def __init__(self, base_types, derivative_types=[]):
        """

        Parameters
        ----------
        base_types : List[tenzing_type]
            The collection of tenzing types at the root of the relations graph

        derivative_types: List[tenzing_type]
            The collection of tenzing types which are derived either from a base_type or themselves

        Returns
        -------
        self

        """
        self.base_types = frozenset(base_types)
        self.derivative_types = frozenset(derivative_types)
        self.types = set(list(self.base_types | self.derivative_types))

        self.relation_map = build_relation_graph(self.base_types, self.derivative_types)


class tenzingTypeset(tenzing_typeset):
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
    def __init__(self, base_types, derivative_types=[]):
        self.column_summary = {}
        super().__init__(base_types, derivative_types)

    def prep(self, df):
        self.column_type_map = {col: self._get_column_type(df[col]) for col in df.columns}
        self.is_prepped = True
        return self

    def summarize(self, df):
        assert self.is_prepped, "typeset hasn't been prepped for your dataset yet. Call .prep(df)"
        summary = {col: self.column_type_map[col].summarize(df[col]) for col in df.columns}
        self.column_summary = summary
        return self.column_summary

    def general_summary(self, df):
        summary = {}
        summary['Number of Observations'] = df.shape[0]
        summary['Number of Variables'] = df.shape[1]
        return summary

    def summary_report(self, df):
        general_summary = self.general_summary(df)
        column_summary = self.summarize(df)
        return summary_report(self.column_type_map, column_summary, general_summary)

    def infer_types(self, df):
        return {col: self.infer_series_type(df[col]) for col in df.columns}

    def infer_series_type(self, series):
        return infer_type(self.column_type_map[series.name], series, self.relation_map)

    def cast_series_to_inferred_type(self, series):
        return cast_to_inferred_type(series, self.column_type_map[series.name], self.relation_map)

    def cast_to_inferred_types(self, df):
        return pd.DataFrame({col: self.cast_series_to_inferred_type(df[col]) for col in df.columns})

    def _get_column_type(self, series):
        # walk the relation_map to determine which is most uniquely specified
        return traverse_relation_graph(series, self.relation_map)

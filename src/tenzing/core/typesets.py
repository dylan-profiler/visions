import pandas as pd
import networkx as nx
import itertools
import matplotlib.pyplot as plt
from networkx.drawing.nx_agraph import write_dot


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
    generic_name = 'generic'

    relation_graph = nx.DiGraph()
    relation_graph.add_node(generic_name)
    print(relation_graph.nodes)
    relation_graph.add_nodes_from(root_nodes)
    relation_graph.add_edges_from(itertools.product([generic_name], root_nodes))
    relation_graph.add_nodes_from(derivative_nodes)
    relation_graph.add_edges_from([node.edge for s_node in root_nodes for to_node, node in s_node().relations.items()],
                                  weight=0)
    relation_graph.add_edges_from(
        [node.edge for s_node in derivative_nodes for to_node, node in s_node().relations.items()], weight=1)

    relations = {node.edge: {'relationship': node} for s_node in root_nodes for to_node, node in
                 s_node().relations.items()}
    nx.set_edge_attributes(relation_graph, relations)

    relations = {node.edge: {'relationship': node} for s_node in derivative_nodes for to_node, node in
                 s_node().relations.items()}
    nx.set_edge_attributes(relation_graph, relations)

    provided_nodes = set(root_nodes) | set(derivative_nodes)
    undefined_nodes = set(relation_graph.nodes) - ({generic_name} | provided_nodes)
    relation_graph.remove_nodes_from(undefined_nodes)
    relation_graph.remove_nodes_from(list(nx.isolates(relation_graph)))

    # TODO: this should be forced by framework...
    # Relations should be connected...
    # orphaned_nodes = [n for n in provided_nodes if n not in set(relation_graph.nodes)]
    # assert not orphaned_nodes, f'{orphaned_nodes} were isolates in the type relation map and consequently orphaned. Please add some mapping to the orphaned nodes.'
    # cycles = list(nx.simple_cycles(relation_graph))
    # assert len(cycles) == 0, f'Cyclical relations between types {cycles} detected'

    plt.title("Data Model")
    return relation_graph


def traverse_relation_graph(series, G, node='generic'):
    """
    Depth-first search
    """
    for tenz_type in G.successors(node):
        if series in tenz_type:
            return traverse_relation_graph(series, G, tenz_type)
    return node


def get_type_inference_path(base_type, series, G, path=None):
    if path is None:
        path = []
    path.append(base_type)
    for tenz_type in G.successors(base_type):
        if G[base_type][tenz_type]['relationship'].is_relation(series):
            print('Transform', series.name, 'from', base_type, 'to', tenz_type)
            new_series = G[base_type][tenz_type]['relationship'].transform(series)
            return get_type_inference_path(tenz_type, new_series, G, path)
    return path


def infer_type(base_type, series, G):
    path = get_type_inference_path(base_type, series, G)
    return path[-1]


def cast_to_inferred_type(series, base_type, G):
    for tenz_type in G.successors(base_type):
        if G[base_type][tenz_type]['relationship'].is_relation(series):
            print('Cast', series.name, 'from', base_type, 'to', tenz_type)
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

    def __init__(self, base_types, derivative_types=None):
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
        if derivative_types is None:
            derivative_types = []
        self.base_types = frozenset(base_types)
        self.derivative_types = frozenset(derivative_types)
        self.types = set(list(self.base_types | self.derivative_types))
        self.relation_map = build_relation_graph(self.base_types, self.derivative_types)

    def plot(self):
        x = self.relation_map
        # nx.draw(x, nodelist=['generic'], edgelist=[], node_color=['red'], with_labels=False)
        nx.draw(x, node_color=['blue'] * len(x.nodes), with_labels=True)


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

    def __init__(self, base_types, derivative_types=None):
        if derivative_types is None:
            derivative_types = []
        self.column_summary = {}
        super().__init__(base_types, derivative_types)

    def prep(self, df):
        # TODO: imporve this (no new attributes outside of __init__)
        self.column_type_map = {col: self._get_column_type(df[col]) for col in df.columns}
        self.is_prepped = True
        return self

    def summarize(self, df):
        assert self.is_prepped, "typeset hasn't been prepped for your dataset yet. Call .prep(df)"
        summary = {col: self.column_type_map[col].summarize(df[col]) for col in df.columns}
        self.column_summary = summary
        return self.column_summary

    def general_summary(self, df):
        summary = {'n_observations': df.shape[0],
                   'n_variables': df.shape[1],
                   'memory_size': df.memory_usage(index=True, deep=True).sum()}
        return summary

    def summary_report(self, df):
        general_summary = self.general_summary(df)
        column_summary = self.summarize(df)
        return {'types': self.column_type_map, 'columns': column_summary, 'general': general_summary}

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

    def plot(self):
        import networkx as nx
        import matplotlib.pyplot as plt

        G = nx.DiGraph()

        nodes = set()
        for data_type in self.base_types.union(self.derivative_types):
            # __mro__[:-2] are (tenzing_model and object)
            elems = [str(x.__name__) for x in data_type.__mro__[:-2]]
            # 'mixin hack
            elems = [x for x in elems if 'Mixin' not in x]
            nodes = nodes.union(set(elems))
            if len(elems) > 1:
                for x, y in zip(elems, elems[1:]):
                    G.add_edge(y, x, weight=1)

        for node in nodes:
            G.add_node(node)

        # for relation_from, relation_to in self.type_relations:
        #     G.add_edge(relation_from, relation_to, weight=0)

        plt.title("Data Model")

        # Drawing
        elarge = [(u, v) for (u, v, d) in G.edges(data=True) if d["weight"] > 0.5]
        esmall = [(u, v) for (u, v, d) in G.edges(data=True) if d["weight"] <= 0.5]

        G.graph['node'] = {'shape': 'box', 'color': 'red'}
        write_dot(G, "graph_inheritance.dot")

        # plt.axis("off")
        # plt.show()

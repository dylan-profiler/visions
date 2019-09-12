import pandas as pd
import networkx as nx
from networkx.drawing.nx_agraph import write_dot
from tenzing.core.model_implementations.types.tenzing_generic import tenzing_generic


def check_graph_constraints(G):
    cycles = list(nx.simple_cycles(G))
    assert len(cycles) == 0, f"Cyclical relations between types {cycles} detected"

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
    base_types : frozenset
        The collection of tenzing types at the root of the relations graph

    derivative_types: frozenset
        The collection of tenzing types which are derived either from a base_type or themselves

    types: frozenset
        The collection of both base_types and derivative_types
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
        # TODO: raise error if types miss parent
        if derivative_types is None:
            derivative_types = []

        # TODO: reconsider value of this distinction
        self.base_types = frozenset(base_types)
        self.derivative_types = frozenset(derivative_types)
        self.types = set(list(self.base_types | self.derivative_types))

        self.inheritance_graph, self.relation_graph, self.complete_graph = (
            self.build_graphs()
        )

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
        return infer_type(
            self.column_type_map[series.name], series, self.relation_graph
        )

    def cast_series_to_inferred_type(self, series):
        return cast_to_inferred_type(
            series, self.column_type_map[series.name], self.relation_graph
        )

    def _get_column_type(self, series):
        # walk the relation_map to determine which is most uniquely specified
        return traverse_relation_graph(series, self.inheritance_graph)

    def get_mro(self, x):
        """
        Notes
        -------
        Taking the last .__bases__ ignores mixins
        """
        mro = [x]
        last_element = list(x.__bases__)[-1]
        if last_element.__bases__:
            mro += self.get_mro(last_element)
        return mro

    def build_graphs(self):
        """

        Notes
        -------
        [:-1] drops 'tenzing_model'
        """
        nodes = set()
        inheritance_edges = []
        relation_edges = []

        for data_type in self.types:
            inheritance_relations = self.get_mro(data_type)[:-1]
            # inheritance_relations = {str(cls.__name__): cls for cls in inheritance_relations}

            nodes = nodes.union(set(inheritance_relations))
            if len(inheritance_relations) > 1:
                for sub_cls, cls in zip(
                    list(inheritance_relations), list(inheritance_relations)[1:]
                ):
                    inheritance_edges.append((cls, sub_cls))

        assert nodes == set(self.types).union(
            {tenzing_generic}
        ), "All subtypes should be in the typeset"

        for node in nodes:
            for key, relation in node.get_relations().items():
                cls = relation.friend_model
                ref_cls = relation.model
                relation_edges.append((cls, ref_cls, relation))

        # TODO: warn if inheritance has also relations

        inheritance_graph = nx.DiGraph()
        relation_graph = nx.DiGraph()
        complete_graph = nx.DiGraph()
        for node in nodes:
            inheritance_graph.add_node(node)
            relation_graph.add_node(node)
            complete_graph.add_node(node)

        for cls, sub_cls in inheritance_edges:
            inheritance_graph.add_edge(cls, sub_cls)
            complete_graph.add_edge(cls, sub_cls)

        for cls, ref_cls, relation in relation_edges:
            relation_graph.add_edge(cls, ref_cls, relationship=relation)
            complete_graph.add_edge(cls, ref_cls, style="dashed", relationship=relation)

        return inheritance_graph, relation_graph, complete_graph

    def write_dot(self):
        for G, file_name in [
            (self.inheritance_graph, "graph_inheritance.dot"),
            (self.relation_graph, "graph_relations.dot"),
            (self.complete_graph, "graph_complete.dot"),
        ]:
            G.graph["node"] = {"shape": "box", "color": "red"}
            write_dot(G, file_name)

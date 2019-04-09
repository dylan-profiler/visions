from tenzing.summary import summary_report
import networkx as nx
import itertools


def build_relation_graph(root_nodes, derivative_nodes):
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


def infer_type(base_type, series, G):
    for tenz_type in G.successors(base_type):
        if G[base_type][tenz_type]['relationship'].is_relation(series):
            new_series = G[base_type][tenz_type]['relationship'].transform(series)
            return infer_type(tenz_type, new_series, G)
    return base_type


class tenzing_typeset:
    def __init__(self, base_types, derivative_types=[]):
        self.base_types = frozenset(base_types)
        self.derivative_types = frozenset(derivative_types)

        self.relation_map = build_relation_graph(self.base_types, self.derivative_types)


class tenzingTypeset(tenzing_typeset):
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

    def _get_column_type(self, series):
        # walk the relation_map to determine which is most uniquely specified
        return traverse_relation_graph(series, self.relation_map)

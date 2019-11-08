# https://bl.ocks.org/fdlk/076469462d00ba39960f854df9acda56

import json
from pathlib import Path

import networkx as nx
from networkx.readwrite import json_graph

from visions.core.implementations.typesets import visions_complete_set

typeset = visions_complete_set()
graph = typeset.base_graph.copy()
nx.relabel_nodes(graph, {n: str(n) for n in graph.nodes}, copy=False)


def update(data):
    data['name'] = data.pop('id')
    if 'children' not in data:
        data['size'] = 1
    else:
        data['children'] = [update(child) for child in data['children']]
    return data


data = json_graph.tree_data(graph, root='visions_generic')

data = update(data)

# TODO:
with Path('typesets/typeset_complete_base.json').open('w') as f:
    json.dump(data, f)

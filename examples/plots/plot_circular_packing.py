import json
from pathlib import Path

import networkx as nx
from networkx.readwrite import json_graph

from visions.core.implementations.typesets import visions_complete_set

typeset = visions_complete_set()
graph = typeset.base_graph.copy()
nx.relabel_nodes(graph, {n: str(n) for n in graph.nodes}, copy=False)


def update(data):
    data["name"] = data.pop("id")
    if "children" not in data:
        data["size"] = 1
    else:
        data["children"] = [update(child) for child in data["children"]]
    return data


data = json_graph.tree_data(graph, root="visions_generic")

data = update(data)

# TODO: write to circular_packing.html
with Path("typesets/typeset_complete_base.json").open("w") as f:
    json.dump(data, f)

import json
import re
from pathlib import Path
from itertools import chain

import networkx as nx

from visions.typesets import CompleteSet


def update(data):
    data["name"] = data.pop("id")
    if "children" not in data:
        data["size"] = 1
    else:
        data["children"] = [update(child) for child in data["children"]]
    return data


def write_html(data, output_file):
    jdata = json.dumps(data)
    string = f"\n\troot = {jdata};\n\t"

    file_name = Path(__file__).parent / "circular_packing.html"
    out_file = Path(output_file)
    fc = file_name.read_text()
    fc = re.sub(
        r"// START-REPLACE(.*)// END-REPLACE",
        rf"// START-REPLACE{string}// END-REPLACE",
        fc,
        flags=re.MULTILINE | re.DOTALL,
    )
    out_file.write_text(fc)


def to_json_tree_sorted(G, root):
    # json_graph.tree_data with sorting
    def add_children(n, G):
        nbrs = G[n]
        if len(nbrs) == 0:
            return []
        children_ = []
        for child in nbrs:
            d = dict(chain(G.nodes[child].items(), [("id", child)]))
            c = add_children(child, G)
            if c:
                d["children"] = c
            children_.append(d)

        children_ = sorted(children_, key=lambda x: x["id"])
        return children_

    data = dict(chain(G.nodes[root].items(), [("id", root)]))
    data["children"] = add_children(root, G)
    return data


def plot_graph_circular_packing(typeset, output_file) -> None:
    graph = typeset.base_graph.copy()
    nx.relabel_nodes(graph, {n: str(n) for n in graph.nodes}, copy=False)

    data = to_json_tree_sorted(graph, root=str(typeset.root_node))
    data = update(data)
    write_html(data, output_file)


if __name__ == "__main__":
    complete_set = CompleteSet()
    plot_graph_circular_packing(complete_set, "circular_packing.html")

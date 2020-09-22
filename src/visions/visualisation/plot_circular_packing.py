import json
import re
from pathlib import Path

import networkx as nx

from visions.typesets import CompleteSet


def update(data):
    data["name"] = data.pop("id")
    if "children" not in data:
        data["size"] = 1
    else:
        data["children"] = [update(child) for child in data["children"]]
    return data


def write_json(data):
    with Path("typesets/typeset_complete_base.json").open("w") as f:
        json.dump(data, f)


def write_html(data):
    string = "\n\troot = {jdata};\n\t".format(jdata=json.dumps(data))

    file_name = Path("circular_packing.html")
    fc = file_name.read_text()
    fc = re.sub(
        r"// START-REPLACE(.*)// END-REPLACE",
        r"// START-REPLACE{string}// END-REPLACE".format(string=string),
        fc,
        flags=re.MULTILINE | re.DOTALL,
    )
    file_name.write_text(fc)


def to_json_tree_sorted(G, root):
    # json_graph.tree_data with sorting
    from itertools import chain

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


def write_circular_packing_files() -> None:
    typeset = CompleteSet()
    graph = typeset.base_graph.copy()
    nx.relabel_nodes(graph, {n: str(n) for n in graph.nodes}, copy=False)

    data = to_json_tree_sorted(graph, root="Generic")
    data = update(data)

    write_json(data)
    write_html(data)


if __name__ == "__main__":
    write_circular_packing_files()

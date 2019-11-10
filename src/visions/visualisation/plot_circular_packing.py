import json
import re
from pathlib import Path

import networkx as nx
from networkx.readwrite import json_graph

from visions.core.implementations.typesets import visions_complete_set


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
    string = f"\n\troot = {json.dumps(data)}\n\t"

    file_name = Path("circular_packing.html")
    fc = file_name.read_text()
    fc = re.sub(
        r"// START-REPLACE(.*)// END-REPLACE",
        f"// START-REPLACE{string}// END-REPLACE",
        fc,
        flags=re.MULTILINE | re.DOTALL,
    )
    file_name.write_text(fc)


def main():
    typeset = visions_complete_set()
    graph = typeset.base_graph.copy()
    nx.relabel_nodes(graph, {n: str(n) for n in graph.nodes}, copy=False)

    data = json_graph.tree_data(graph, root="visions_generic")

    data = update(data)

    write_json(data)
    write_html(data)


if __name__ == "__main__":
    main()

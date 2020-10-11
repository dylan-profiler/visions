from pathlib import Path
from typing import Union

import networkx as nx


def output_graph(
    G: nx.DiGraph, file_name: Union[Path, str], sort: bool = True, file_format=None
) -> None:
    """Output a graph to a file, either as image or as dot file.

    Args:
        G: the DiGraph to write or plot
        file_name: the file name to write to.
        sort: create a copy of the graph with sorted keys
        file_format: graphviz output format, if None, the file_name extension is used as format
            https://graphviz.org/doc/info/output.html

    Returns:
        Nothing

    Raises:
        ValueError when the file_name does not end on .svg, .png or .dot
    """

    if sort:
        # Create ordered graph for deterministic image outputs
        G_sorted = nx.DiGraph()
        G_sorted.graph["node"] = {"shape": "box", "color": "red"}
        G_sorted.add_nodes_from(sorted(G.nodes, key=lambda x: str(x)))

        style = nx.get_edge_attributes(G, "style")
        for edge in sorted(G.edges, key=lambda x: (str(x[0]), str(x[1]))):
            G_sorted.add_edge(*edge, style=style.get(edge))
        G = G_sorted

    p = nx.drawing.nx_pydot.to_pydot(G)
    if not isinstance(file_name, Path):
        file_name = Path(file_name)

    if file_format is None:
        file_format = file_name.suffix[1:].lower()

    try:
        p.write(file_name, format=file_format)
    except AssertionError:
        raise ValueError(
            "Could not write file. Please make sure that the format is accepted by pydot."
        )

from pathlib import Path
from typing import Union

import networkx as nx


def output_graph(G: nx.DiGraph, file_name: Union[Path, str]) -> None:
    """Output a graph to a file, either as image or as dot file.

    Args:
        G: the DiGraph to write or plot
        file_name: the file name to write to. Extension can be svg, png or dot.

    Returns:
        Nothing

    Raises:
        ValueError when the file_name does not end on .svg, .png or .dot
    """
    p = nx.drawing.nx_pydot.to_pydot(G)
    if not isinstance(file_name, Path):
        file_name = Path(file_name)

    if file_name.suffix == ".svg":
        p.write_svg(file_name)
    elif file_name.suffix == ".png":
        p.write_png(file_name)
    elif file_name.suffix == ".dot":
        p.write_dot(file_name)
    else:
        raise ValueError("Extension should be .dot, .svg or .png")

from pathlib import Path
import networkx as nx


def output_graph(G, file_name):
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

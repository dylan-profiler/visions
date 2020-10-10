from pathlib import Path

from visions.typesets import CompleteSet, GeometrySet, StandardSet

# Windows Note
# Tip for Python3/64-bit compatible version of pygraphviz
# https://github.com/CristiFati/Prebuilt-Binaries/raw/master/Windows/PyGraphviz/pygraphviz-1.5-cp37-cp37m-win_amd64.whl


def generate_typeset_plots() -> None:
    typesets_dir = Path("typesets/")
    typesets_dir.mkdir(exist_ok=True)

    # Initialize typeset
    for name, tsc in [
        ("typeset_complete", CompleteSet()),
        ("typeset_geometry", GeometrySet()),
        ("typeset_standard", StandardSet()),
    ]:
        # Write graph to dot
        tsc.output_graph(typesets_dir / f"{name}.dot")

        # Plot the graph (svg)
        tsc.output_graph(typesets_dir / f"{name}.svg")
        tsc.output_graph(typesets_dir / f"{name}_base.svg", base_only=True)

        # Plot the graph (pdf)
        tsc.output_graph(typesets_dir / f"{name}.pdf")
        tsc.output_graph(typesets_dir / f"{name}_base.pdf", base_only=True)

        # Plot the graph (png)
        tsc.output_graph(typesets_dir / f"{name}.png", dpi=150)


if __name__ == "__main__":
    generate_typeset_plots()

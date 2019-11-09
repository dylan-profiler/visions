from pathlib import Path

from visions.core.implementations.typesets import (
    visions_complete_set,
    visions_standard_set,
    visions_geometry_set,
)

# Windows Note
# Tip for Python3/64-bit compatible version of pygraphviz
# https://github.com/CristiFati/Prebuilt-Binaries/raw/master/Windows/PyGraphviz/pygraphviz-1.5-cp37-cp37m-win_amd64.whl


typesets_dir = Path("typesets/")
typesets_dir.mkdir(exist_ok=True)

# Initialize typeset
for name, tsc in [
    ("typeset_complete", visions_complete_set()),
    ("typeset_geometry", visions_geometry_set()),
    ("typeset_standard", visions_standard_set()),
]:
    # Write graph to dot
    tsc.output_graph(typesets_dir / f"{name}.dot")

    # Plot the graph (svg)
    tsc.output_graph(typesets_dir / f"{name}.svg")
    tsc.output_graph(typesets_dir / f"{name}_base.svg", base_only=True)

    # Plot the graph (png)
    tsc.output_graph(typesets_dir / f"{name}.png")

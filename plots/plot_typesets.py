from pathlib import Path

from tenzing.core.model.typesets import (
    tenzing_complete_set,
    tenzing_standard_set,
    tenzing_geometry_set,
)

# Windows Note
# Tip for Python3/64-bit compatible version of pygraphviz
# https://github.com/CristiFati/Prebuilt-Binaries/raw/master/Windows/PyGraphviz/pygraphviz-1.5-cp37-cp37m-win_amd64.whl


typesets_dir = Path("typesets/")
typesets_dir.mkdir(exist_ok=True)

# Initialize typeset
for name, tsc in [
    ("typeset_complete", tenzing_complete_set()),
    ("typeset_geometry", tenzing_geometry_set()),
    ("typeset_standard", tenzing_standard_set()),
]:
    # Write graph to dot
    tsc.output_graph(typesets_dir / f"{name}.dot")

    # Plot the graph (svg)
    tsc.output_graph(typesets_dir / f"{name}.svg")

    # Plot the graph (png)
    tsc.output_graph(typesets_dir / f"{name}.png")

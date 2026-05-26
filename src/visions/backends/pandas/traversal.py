from typing import Dict, List, Tuple, Type

import networkx as nx
import pandas as pd

from visions.types.type import VisionsBaseType
from visions.typesets.typeset import traverse_graph, traverse_graph_with_series

T = type[VisionsBaseType]


@traverse_graph.register(pd.Series)
def _traverse_graph_series(
    series: pd.Series, root_node: T, graph: nx.DiGraph
) -> tuple[pd.Series, list[T], dict]:
    return traverse_graph_with_series(root_node, series, graph)


@traverse_graph.register(pd.DataFrame)
def _traverse_graph_dataframe(
    df: pd.DataFrame, root_node: T, graph: nx.DiGraph
) -> tuple[pd.DataFrame, dict[str, list[T]], dict[str, dict]]:
    inferred_values = {
        col: traverse_graph(df[col], root_node, graph) for col in df.columns
    }

    inferred_series = {}
    inferred_paths: dict[str, list[T]] = {}
    inferred_states: dict[str, dict] = {}
    for col, (inf_series, inf_path, inf_state) in inferred_values.items():
        assert isinstance(inf_path, list)  # Placate the MyPy Gods

        inferred_series[col] = inf_series
        inferred_paths[col] = inf_path
        inferred_states[col] = inf_state

    return pd.DataFrame(inferred_series), inferred_paths, inferred_states

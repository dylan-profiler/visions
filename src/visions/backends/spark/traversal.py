from typing import Dict, List, Tuple, Type

import networkx as nx
import pandas as pd
from pyspark.sql.column import Column
from pyspark.sql.dataframe import DataFrame

from visions.types.type import VisionsBaseType
from visions.typesets.typeset import traverse_graph, traverse_graph_with_series

T = Type[VisionsBaseType]


@traverse_graph.register(Column)
def _traverse_graph_series(
    series: Column, root_node: T, graph: nx.DiGraph
) -> Tuple[Column, List[T], dict]:
    return traverse_graph_with_series(root_node, series, graph)


@traverse_graph.register(DataFrame)
def _traverse_graph_spark_dataframe(
    df: DataFrame, root_node: T, graph: nx.DiGraph
) -> Tuple[DataFrame, Dict[str, List[T]], Dict[str, dict]]:
    inferred_values = {
        col: traverse_graph(df[col], root_node, graph) for col in df.columns
    }

    inferred_series = {}
    inferred_paths: Dict[str, List[T]] = {}
    inferred_states: Dict[str, dict] = {}
    for col, (inf_series, inf_path, inf_state) in inferred_values.items():
        assert isinstance(inf_path, list)  # Placate the MyPy Gods

        inferred_series[col] = inf_series
        inferred_paths[col] = inf_path
        inferred_states[col] = inf_state

    # note inference disabled, return df
    return df, inferred_paths, inferred_states

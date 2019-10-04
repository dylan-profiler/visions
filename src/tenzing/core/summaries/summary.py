import pandas as pd
import networkx as nx

from tenzing.core.model import tenzing_complete_set
from tenzing.core.model.models import tenzing_model
from tenzing.core.model.types import *
from tenzing.core.summaries import *
from tenzing.utils.graph import output_graph


class Summary(object):
    def __init__(self, summary_ops, typeset):
        """

        Args:
            summary_ops:
            typeset:
        """
        self.typeset = typeset
        if summary_ops is None:
            summary_ops = {}

        if not all(
            issubclass(base_type, tenzing_model) for base_type in summary_ops.keys()
        ):
            raise Exception("Summaries must be mapped on a type!")

        self.summary_ops = summary_ops

    def summarize_frame(self, df: pd.DataFrame):
        """

        Args:
            df:

        Returns:

        """
        return dataframe_summary(df)

    def summarize_series(self, series: pd.Series, summary_type: tenzing_model) -> dict:
        """

        Args:
            series:
            summary_type:

        Returns:

        """
        summary = {}

        done = []
        for base_type, summary_ops in self.summary_ops.items():
            if (
                base_type not in done
                and issubclass(summary_type, base_type)
                and not isinstance(summary_type, tenzing_model)
            ):
                for op in summary_ops:
                    summary.update(op(series))
                done.append(base_type)

        return summary

    def summarize(self, df: pd.DataFrame, types) -> dict:
        """

        Args:
            df:
            types:

        Returns:

        """
        frame_summary = self.summarize_frame(df)
        series_summary = {
            col: self.summarize_series(df[col], types[col]) for col in df.columns
        }
        return {"types": types, "series": series_summary, "frame": frame_summary}

    def plot(self, file_name, type_specific=None):
        """

        Args:
            file_name:
            type_specific:

        Returns:

        """
        G = self.typeset.relation_graph.copy()
        G.graph["node"] = {"shape": "box", "color": "red"}

        # Drop dashed relations
        G.remove_edges_from(
            [
                (start, end)
                for start, end, attributes in G.edges(data=True)
                if attributes["style"] == "dashed"
            ]
        )

        included_nodes = G.nodes
        if type_specific is not None:
            leave = nx.ancestors(G, type_specific)

            included_nodes = leave
            G.remove_nodes_from(G.nodes - leave)

        G.add_node("summary", shape="note")
        for base_type, summary_ops in self.summary_ops.items():
            if len(summary_ops) > 0 and base_type in included_nodes:
                G.add_edge(
                    str(base_type),
                    "summary",
                    label="\n".join([str(op.__name__) for op in summary_ops]),
                )

        output_graph(G, file_name)


type_summary_ops = {
    tenzing_bool: [],
    tenzing_categorical: [category_summary, unique_summary],
    tenzing_complex: [infinite_summary, complex_summary, unique_summary_complex],
    tenzing_datetime: [range_summary, unique_summary],
    tenzing_date: [],
    tenzing_existing_path: [existing_path_summary, path_summary, text_summary],
    tenzing_float: [infinite_summary, numerical_summary, zero_summary, unique_summary],
    tenzing_geometry: [],
    tenzing_image_path: [],
    tenzing_integer: [
        infinite_summary,
        numerical_summary,
        zero_summary,
        unique_summary,
    ],
    tenzing_object: [unique_summary],
    tenzing_path: [path_summary, text_summary],
    tenzing_string: [text_summary, unique_summary],
    tenzing_time: [],
    tenzing_timedelta: [],
    tenzing_url: [url_summary, unique_summary],
    tenzing_generic: [base_summary, missing_summary],
}

# TODO: add typeset
typeset = tenzing_complete_set()
summary = Summary(type_summary_ops, typeset)

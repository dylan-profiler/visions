from typing import Union

import pandas as pd

from tenzing.core.models import tenzing_model, MultiModel
from tenzing.core.model.types import *
from tenzing.core.summaries import *


class Summary(object):
    def __init__(self, summary_ops):
        if summary_ops is None:
            summary_ops = {}

        if not all(issubclass(base_type, tenzing_model) for base_type in summary_ops.keys()):
            raise Exception("Summaries must be mapped on a type!")

        self.summary_ops = summary_ops

    def summarize_frame(self, df: pd.DataFrame):
        return dataframe_summary(df)

    def summarize_series(self, series: pd.Series, summary_type: Union[tenzing_model, MultiModel]) -> dict:
        summary = {}

        if isinstance(summary_type, MultiModel):
            types = summary_type.models
        else:
            types = [summary_type]

        done = []
        for current_type in types:
            for base_type, summary_ops in self.summary_ops.items():
                if base_type not in done and issubclass(current_type, base_type) and not isinstance(current_type, tenzing_model):
                    mask = base_type.mask(series)
                    print(series.to_dict(), mask.to_dict())
                    for op in summary_ops:
                        print(f"summarizing {current_type} though {base_type} via {op.__name__}")
                        summary.update(op(series[mask]))
                    done.append(base_type)

        return summary

    def summarize(self, df: pd.DataFrame, types) -> dict:
        frame_summary = self.summarize_frame(df)
        series_summary = {
            col: self.summarize_series(df[col], types[col]) for col in df.columns
        }
        return {"types": types, "series": series_summary, "frame": frame_summary}


type_summary_ops = {
    tenzing_bool: [],
    tenzing_categorical: [category_summary, unique_summary],
    tenzing_complex: [complex_summary, unique_summary],
    tenzing_datetime: [datetime_summary, unique_summary],
    tenzing_date: [],
    tenzing_existing_path: [existing_path_summary, path_summary, text_summary],
    tenzing_float: [numerical_summary, zero_summary, unique_summary],
    tenzing_geometry: [],
    tenzing_image_path: [],
    tenzing_integer: [numerical_summary, zero_summary, unique_summary],
    tenzing_object: [unique_summary],
    tenzing_path: [path_summary, text_summary],
    tenzing_string: [text_summary],
    tenzing_time: [],
    tenzing_timedelta: [],
    tenzing_url: [url_summary, unique_summary],
    infinite_generic: [infinite_summary],
    missing_generic: [missing_summary],
    tenzing_generic: [],
    tenzing_model: [base_summary]
}

# TODO: add typeset
summary = Summary(type_summary_ops)

import pandas as pd
from tenzing.core.model_implementations.compound_type import CompoundType

from tenzing.core.model_implementations.sub_types import missing, infinite

from tenzing.core.model_implementations.types import (
    tenzing_url,
    tenzing_timedelta,
    tenzing_time,
    tenzing_string,
    tenzing_path,
    tenzing_object,
    tenzing_integer,
    tenzing_image_path,
    tenzing_geometry,
    tenzing_float,
    tenzing_existing_path,
    tenzing_date,
    tenzing_datetime,
    tenzing_complex,
    tenzing_categorical,
    tenzing_bool,
    tenzing_generic,
)


from tenzing.core.models import tenzing_model
from tenzing.core.summaries import (
    category_summary,
    unique_summary,
    complex_summary,
    datetime_summary,
    existing_path_summary,
    path_summary,
    text_summary,
    numerical_summary,
    zero_summary,
    url_summary,
    missing_summary,
    infinite_summary,
    base_summary,
)


class Summary(object):
    def __init__(self, type_summary_ops):
        if type_summary_ops is None:
            type_summary_ops = {}

        self.type_summary_ops = type_summary_ops

    def summarize_series(self, series: pd.Series, type: tenzing_model) -> dict:
        summary = {}

        # Basetype
        if tenzing_generic in self.type_summary_ops:
            for op in self.type_summary_ops[tenzing_generic]:
                summary.update(op(series))

        if not isinstance(type, CompoundType):
            type = CompoundType(type)

        # Detected type
        mask = type.get_mask(series)
        if type.base_type in self.type_summary_ops:
            for op in self.type_summary_ops[type.base_type]:
                summary.update(op(series[~mask]))

        # Subtypes
        for subtype in type.types:
            if subtype in self.type_summary_ops:
                for op in self.type_summary_ops[subtype]:
                    summary.update(op(series))
        return summary


type_summary_ops = {
    tenzing_generic: [base_summary],
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
    infinite: [infinite_summary],
    missing: [missing_summary],
}

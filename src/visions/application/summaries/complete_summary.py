from visions.types import *
from visions.typesets import visions_complete_set
from visions.application.summaries.summary import Summary
from visions.application.summaries import *


class CompleteSummary(Summary):
    def __init__(self):
        type_summary_ops = {
            visions_bool: [],
            visions_categorical: [category_summary, unique_summary],
            visions_complex: [
                infinite_summary,
                numerical_basic_summary,
                unique_summary_complex,
            ],
            visions_datetime: [range_summary, unique_summary],
            visions_date: [],
            visions_existing_path: [existing_path_summary, path_summary, text_summary],
            visions_float: [
                infinite_summary,
                numerical_summary,
                zero_summary,
                unique_summary,
            ],
            visions_geometry: [],
            visions_image_path: [],
            visions_integer: [
                infinite_summary,
                numerical_summary,
                zero_summary,
                unique_summary,
            ],
            visions_object: [unique_summary],
            visions_path: [path_summary, text_summary],
            visions_string: [text_summary, unique_summary],
            visions_time: [],
            visions_timedelta: [],
            visions_url: [url_summary, unique_summary],
            visions_generic: [base_summary, missing_summary],
        }
        super().__init__(type_summary_ops, visions_complete_set())

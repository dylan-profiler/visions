from visions.types import *
from visions.typesets import CompleteSet
from visions.application.summaries.summary import Summary
from visions.application.summaries import *


class CompleteSummary(Summary):
    def __init__(self):
        type_summary_ops = {
            Boolean: [],
            Categorical: [category_summary, unique_summary],
            Complex: [
                infinite_summary,
                numerical_basic_summary,
                unique_summary_complex,
            ],
            DateTime: [range_summary, unique_summary],
            Date: [],
            File: [file_summary, path_summary, text_summary],
            Float: [infinite_summary, numerical_summary, zero_summary, unique_summary],
            Geometry: [],
            Image: [image_summary],
            Integer: [
                infinite_summary,
                numerical_summary,
                zero_summary,
                unique_summary,
            ],
            Object: [unique_summary],
            Path: [path_summary, text_summary],
            String: [text_summary, unique_summary],
            Time: [],
            TimeDelta: [],
            UUID: [],
            URL: [url_summary, unique_summary],
            Generic: [base_summary, missing_summary],
        }
        super().__init__(type_summary_ops, CompleteSet())

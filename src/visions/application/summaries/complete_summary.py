from visions.application.summaries.series import (
    base_summary,
    category_summary,
    file_summary,
    image_summary,
    missing_summary,
    numerical_basic_summary,
    numerical_summary,
    path_summary,
    range_summary,
    text_summary,
    unique_summary,
    unique_summary_complex,
    url_summary,
    zero_summary,
)
from visions.application.summaries.summary import Summary
from visions.types import *
from visions.typesets import CompleteSet


class CompleteSummary(Summary):
    def __init__(self) -> None:
        type_summary_ops = {
            Boolean: [],
            Categorical: [category_summary, unique_summary],
            Complex: [numerical_basic_summary, unique_summary_complex],
            DateTime: [range_summary, unique_summary],
            Date: [],
            File: [file_summary, path_summary, text_summary],
            Float: [numerical_summary, zero_summary, unique_summary],
            Geometry: [],
            Image: [image_summary],
            Integer: [numerical_summary, zero_summary, unique_summary],
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

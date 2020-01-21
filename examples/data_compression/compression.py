from pathlib import Path

import pandas as pd
from pandas_profiling import ProfileReport

from visions.core.functional import (
    type_cast_frame,
    type_inference_frame,
    type_detect_frame,
    compare_detect_inference_frame,
    type_inference_report_frame,
)
from visions.application.summaries.summary import CompleteSummary

# file_name = "https://opendata.rdw.nl/api/views/m9d7-ebf2/rows.csv?accessType=DOWNLOAD"
from examples.data_compression.rdw_typeset import rdw_typeset

file_name = Path(
    r"C:\Users\Cees Closed\Documents\code\say-hello\data\rdw\gekentekende_voertuigen.csv"
)

# Load dataset
df = pd.read_csv(file_name, nrows=1000)

# Type
cast_df = type_cast_frame(df, rdw_typeset)

# Type inference
report = type_inference_report_frame(df, rdw_typeset)
print(report)

# Summarization
# summary = CompleteSummary()
# summaries = summary.summarize(cast_df, inferred_types)
# for key, variable_summary in summaries["series"].items():
#     print(key, variable_summary)

# TODO: ordinal
# manual_df["Zuinigheidslabel"] = manual_df["Zuinigheidslabel"].astype(
#     CategoricalDtype(categories=["A", "B", "C", "D", "E", "F", "G"], ordered=True)
# )

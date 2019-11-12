import pandas as pd

from visions.core.implementations import visions_complete_set
from visions.core.functional import type_cast_frame, type_inference_frame
from visions.application.summaries.summary import CompleteSummary


# Load dataset
df = pd.read_csv("https://www.opendisdata.nl/download/csv/01_DBC.csv")
df["JAAR"] = pd.to_datetime(df["JAAR"], format="%Y")

# Type
typeset = visions_complete_set()

# Type inference
inferred_types = type_inference_frame(df, typeset)
print(inferred_types)

# Type cast
cast_df, cast_types = type_cast_frame(df, typeset)
print(cast_types)

# Summarization
summary = CompleteSummary()
summaries = summary.summarize(cast_df, cast_types)
for key, variable_summary in summaries["series"].items():
    print(key, variable_summary)

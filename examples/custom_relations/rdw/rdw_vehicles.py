import pandas as pd

from examples.custom_relations.rdw.rdw_typeset import rdw_typeset
from visions.core.functional import type_cast, type_inference
from visions.core.summaries.summary import CompleteSummary


# file_name = "https://opendata.rdw.nl/api/views/m9d7-ebf2/rows.csv?accessType=DOWNLOAD"
file_name = r"C:\Users\Cees Closed\Downloads\Open_Data_RDW__Gekentekende_voertuigen.csv"

# Load dataset
df = pd.read_csv(file_name, nrows=10000)

# Type
typeset = rdw_typeset()
typeset.output_graph(f"rdw_typeset.svg")

# Type inference
inferred_types = type_inference(df, typeset)
print(inferred_types)

# Type cast
cast_df, cast_types = type_cast(df, typeset)
# print(cast_types)

# Summarization
summary = CompleteSummary()
summaries = summary.summarize(cast_df, cast_types)
# for key, variable_summary in summaries["series"].items():
#     print(key, variable_summary)

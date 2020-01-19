from pathlib import Path

import pandas as pd

from visions.core.implementations import visions_complete_set
from visions.core.functional import type_cast_frame, type_inference_frame
from visions.application.summaries.summary import CompleteSummary


# file_name = "https://opendata.rdw.nl/api/views/m9d7-ebf2/rows.csv?accessType=DOWNLOAD"
file_name = Path(r"C:\Users\Cees Closed\Downloads\Open_Data_RDW__Gekentekende_voertuigen.csv")

# Load dataset
df = pd.read_csv(file_name, nrows=10000)
# print(df.info())
df.to_parquet(file_name.with_suffix('.parquet'))

# Type
typeset = visions_complete_set()

# Type inference
inferred_types = type_inference_frame(df, typeset)
print(inferred_types)

# Type cast
cast_df = type_cast_frame(df, typeset)

# Summarization
# summary = CompleteSummary()
# summaries = summary.summarize(cast_df, inferred_types)
# for key, variable_summary in summaries["series"].items():
#     print(key, variable_summary)



def get_file_size(file_name: Path):
    return file_name.stat().st_size


def get_df_size(df: pd.DataFrame):
    return df.memory_usage(deep=True).sum()


og_subset_name = file_name.parent / "subset.csv"
df.to_csv(og_subset_name, index=False)

new_name = file_name.parent / "blaat.csv"
cast_df.to_csv(new_name, index=False)

og_size = get_file_size(og_subset_name)
cast_size = get_file_size(new_name)
parq = get_file_size(file_name.with_suffix('.parquet'))

# Compare file sizes
print(f"Original file: {og_size}", get_df_size(df))
print(f"Cast file: {cast_size}, reduction of {100 - (cast_size / og_size * 100)}", get_df_size(cast_df))
print(f"Parquet file: {parq}, reduction of {100 - (parq / og_size * 100)}")

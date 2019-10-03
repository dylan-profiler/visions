import pandas as pd

from tenzing.core.model import tenzing_complete_set, type_cast, type_inference
from tenzing.core.summaries.summary import summary


# file_name = "https://opendata.rdw.nl/api/views/m9d7-ebf2/rows.csv?accessType=DOWNLOAD"
file_name = r"C:\Users\Cees Closed\Downloads\Open_Data_Parkeren__SPECIFICATIES_PARKEERGEBIED.csv"

# Load dataset
df = pd.read_csv(
    file_name
)

# Type
typeset = tenzing_complete_set()

# Type inference
inferred_types = type_inference(df, typeset)
print(inferred_types)

# Type cast
cast_df, cast_types = type_cast(df, typeset)
print(cast_types)

# Summarization
# summaries = summary.summarize(cast_df, cast_types)
# for key, variable_summary in summaries["series"].items():
#     print(key, variable_summary)
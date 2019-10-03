import pandas as pd

from tenzing.core.model import tenzing_complete_set
from tenzing.core.summaries.summary import summary

# Load dataset
df = pd.read_csv(
    "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
)

# Type
x = tenzing_complete_set()
y = tenzing_complete_set()
x.prep(df)

# Type inference
tdf = x.cast_to_inferred_types(df)

print(x.column_type_map)
y.prep(tdf)
print(y.column_type_map)

# Summarization
x = summary.summarize(df, x.column_type_map)
for key, variable_summary in x["series"].items():
    print(key, variable_summary)

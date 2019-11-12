import pandas as pd

from visions.core.implementations import visions_complete_set
from visions.core.functional import type_cast_frame, type_inference_frame
from visions.application.summaries.summary import CompleteSummary
from visions.core.model.dtypes.bool_fix.visions_bool import visions_boolean

# Load dataset
df = pd.read_csv(
    "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
)

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

print(summaries["frame"])

from visions.core.implementations.types import (
    visions_float,
    visions_integer,
    visions_categorical,
    visions_string,
    visions_ordinal,
)

# These are the "raw" data types as we load them
before_cast = {
    "Age": visions_float,
    "Cabin": visions_string,
    "Embarked": visions_string,
    "Fare": visions_float,
    "Name": visions_string,
    "Parch": visions_integer,
    "SibSp": visions_integer,
    "PassengerId": visions_integer,
    "Pclass": visions_integer,
    "Sex": visions_string,
    "Survived": visions_integer,
    "Ticket": visions_string,
}

# These are the types that are inferred
after_cast = {
    "Age": visions_float,
    "Cabin": visions_categorical,
    "Embarked": visions_categorical,
    "Fare": visions_float,
    "Name": visions_string,  # Unique
    "Parch": visions_integer,  # Count
    "SibSp": visions_integer,  # Count
    "PassengerId": visions_integer,
    "Pclass": visions_ordinal,
    "Sex": visions_categorical,
    "Survived": visions_boolean,
    "Ticket": visions_categorical,
}

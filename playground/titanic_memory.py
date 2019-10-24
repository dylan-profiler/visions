import pandas as pd
import numpy as np

from visions.core.model import visions_complete_set, type_cast, type_inference
from visions.core.model.dtypes.bool_fix.visions_bool import visions_boolean

# Load dataset
df = pd.read_csv(
    "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
)

start = df.memory_usage(deep=True).sum()

df["Survived"] = df["Survived"].astype(bool)
df["Fare"] = df["Fare"].astype(np.float16)
df["Age"] = df["Age"].astype(np.float16)
df["SibSp"] = df["SibSp"].astype(np.uint8)
df["Parch"] = df["Parch"].astype(np.uint8)
df["Parch"] = df["Parch"].astype(np.uint8)
df["PassengerId"] = df["PassengerId"].astype(np.uint8)
df["Pclass"] = pd.Categorical(
    df["Pclass"], categories=sorted(df["Pclass"].unique()), ordered=True
)

end = df.memory_usage(deep=True).sum()

print(
    f"Initial {start} bytes reduced to {end} bytes. Difference {start - end} bytes. Reduction of {(start-end) / start:.0%}"
)

# Type
typeset = visions_complete_set()

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

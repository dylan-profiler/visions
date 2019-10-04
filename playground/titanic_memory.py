import pandas as pd
import numpy as np

from tenzing.core.model import tenzing_complete_set, type_cast, type_inference
from tenzing.core.model.dtypes.bool_fix.tenzing_bool import tenzing_boolean
from tenzing.core.summaries.summary import summary

# Load dataset
df = pd.read_csv(
    "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
)

start = df.memory_usage(deep=True).sum()

df['Survived'] = df['Survived'].astype(bool)
df['Fare'] = df['Fare'].astype(np.float16)
df['Age'] = df['Age'].astype(np.float16)
df['SibSp'] = df['SibSp'].astype(np.uint8)
df['Parch'] = df['Parch'].astype(np.uint8)
df['Parch'] = df['Parch'].astype(np.uint8)
df['PassengerId'] = df['PassengerId'].astype(np.uint8)
df['Pclass'] = pd.Categorical(df['Pclass'], categories=sorted(df['Pclass'].unique()), ordered=True)

end = df.memory_usage(deep=True).sum()

print(f"Initial {start} bytes reduced to {end} bytes. Difference {start - end} bytes. Reduction of {(start-end) / start:.0%}")

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


from tenzing.core.model.types import tenzing_float, tenzing_integer, tenzing_categorical, tenzing_string, \
    tenzing_ordinal

# These are the "raw" data types as we load them
before_cast = {
    'Age': tenzing_float,
    'Cabin': tenzing_string,
    'Embarked': tenzing_string,
    'Fare': tenzing_float,
    'Name': tenzing_string,
    'Parch': tenzing_integer,
    'SibSp': tenzing_integer,
    'PassengerId': tenzing_integer,
    'Pclass': tenzing_integer,
    'Sex': tenzing_string,
    'Survived': tenzing_integer,
    'Ticket': tenzing_string,
}

# These are the types that are inferred
after_cast = {
    'Age': tenzing_float,
    'Cabin': tenzing_categorical,
    'Embarked': tenzing_categorical,
    'Fare': tenzing_float,
    'Name': tenzing_string, # Unique
    'Parch': tenzing_integer, # Count
    'SibSp': tenzing_integer, # Count
    'PassengerId': tenzing_integer,
    'Pclass': tenzing_ordinal,
    'Sex': tenzing_categorical,
    'Survived': tenzing_boolean,
    'Ticket': tenzing_categorical,
}
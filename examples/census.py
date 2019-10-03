from pathlib import Path

import pandas as pd

from tenzing.core.model import tenzing_complete_set
from tenzing.core.summaries.summary import summary

if __name__ == "__main__":
    file_name = Path("census_train.csv")

    # Names based on https://archive.ics.uci.edu/ml/machine-learning-databases/adult/adult.names
    df = pd.read_csv(
        file_name,
        header=None,
        index_col=False,
        names=[
            "age",
            "workclass",
            "fnlwgt",
            "education",
            "education-num",
            "marital-status",
            "occupation",
            "relationship",
            "race",
            "sex",
            "capital-gain",
            "capital-loss",
            "hours-per-week",
            "native-country",
        ],
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

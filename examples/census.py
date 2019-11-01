from pathlib import Path

import pandas as pd

from visions.core.implementations import visions_complete_set
from visions.core.functional import type_cast, type_inference
from visions.core.summaries.summary import CompleteSummary

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
    typeset = visions_complete_set()

    # Type inference
    inferred_types = type_inference(df, typeset)
    print(inferred_types)

    # Type cast
    cast_df, cast_types = type_cast(df, typeset)
    print(cast_types)

    # Summarization
    summary = CompleteSummary()
    summaries = summary.summarize(cast_df, cast_types)
    for key, variable_summary in summaries["series"].items():
        print(key, variable_summary)

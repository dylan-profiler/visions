from pprint import pprint

import numpy as np
import pandas as pd

import visions as v
from visions.application.summaries import CompleteSummary

category_series = pd.Series(
    pd.Categorical(
        [True, False, np.nan, "test"], categories=[True, False, "test", "missing"]
    )
)

# Generate a summary
summarizer = CompleteSummary()
summary = summarizer.summarize_series(category_series, v.Categorical)

pprint(summary)

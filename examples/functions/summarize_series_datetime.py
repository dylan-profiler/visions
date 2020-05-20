from pprint import pprint

import numpy as np
import pandas as pd

import visions as v
from visions.application.summaries import CompleteSummary

datetime_series = pd.Series(
    [
        pd.datetime(2010, 1, 1),
        pd.datetime(2010, 8, 2),
        pd.datetime(2011, 2, 1),
        np.datetime64("NaT"),
    ]
)

# Generate a summary
summarizer = CompleteSummary()
summary = summarizer.summarize_series(datetime_series, v.DateTime)

pprint(summary)

from pprint import pprint

import pandas as pd
import numpy as np

from visions.application.summaries.summary import CompleteSummary
from visions.core.implementations.types import visions_datetime

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
summary = summarizer.summarize_series(datetime_series, visions_datetime)

pprint(summary)

from pprint import pprint

import pandas as pd
import numpy as np

from visions.application.summaries.summary import CompleteSummary
from visions.core.implementations.types import visions_categorical

category_series = pd.Series(
    pd.Categorical(
        [True, False, np.nan, "test"], categories=[True, False, "test", "missing"]
    )
)

# Generate a summary
summarizer = CompleteSummary()
summary = summarizer.summarize_series(category_series, visions_categorical)

pprint(summary)

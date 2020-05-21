import numpy as np
import pandas as pd

from visions import types as v
from visions.application.summaries import CompleteSummary

datetime_series = pd.Series(
    [
        pd.datetime(2010, 1, 1),
        pd.datetime(2010, 8, 2),
        pd.datetime(2011, 2, 1),
        np.datetime64("NaT"),
    ]
)

summarizer = CompleteSummary()
summary = summarizer.summarize_series(datetime_series, v.DateTime)
print(summary)

# Output:
# {
#     "dtype": dtype("<M8[ns]"),
#     "frequencies": {
#         Timestamp("2010-01-01 00:00:00"): 1,
#         Timestamp("2010-08-02 00:00:00"): 1,
#         Timestamp("2011-02-01 00:00:00"): 1,
#     },
#     "max": Timestamp("2011-02-01 00:00:00"),
#     "memory_size": 160,
#     "min": Timestamp("2010-01-01 00:00:00"),
#     "n_records": 4,
#     "n_unique": 3,
#     "na_count": 1,
#     "range": Timedelta("396 days 00:00:00"),
#     "types": {"NaTType": 1, "Timestamp": 3},
# }

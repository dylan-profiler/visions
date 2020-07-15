import numpy as np
import pandas as pd

from visions import types as vt
from visions.application.summaries import CompleteSummary

integer_series = pd.Series([1, 2, 3, 4, 5, -100000, np.nan], dtype="Int64")

summarizer = CompleteSummary()
summary = summarizer.summarize_series(integer_series, vt.Integer)
print(summary)

# Output:
# {
#     "inf_count": 0,
#     "mean": -16664.166666666668,
#     "std": 40826.05381575185,
#     "var": 1666766670.1666665,
#     "max": 5.0,
#     "min": -100000.0,
#     "median": 2.5,
#     "kurt": 5.999999974801513,
#     "skew": -2.449489736169953,
#     "sum": -99985.0,
#     "mad": 27778.611111111113,
#     "quantile_5": -74999.75,
#     "quantile_25": 1.25,
#     "quantile_50": 2.5,
#     "quantile_75": 3.75,
#     "quantile_95": 4.75,
#     "iqr": 2.5,
#     "range": 100005.0,
#     "cv": -2.449930718552894,
#     "monotonic_increase": False,
#     "monotonic_decrease": False,
#     "n_zeros": 0,
#     "n_unique": 6,
#     "frequencies": {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, -100000: 1},
#     "n_records": 7,
#     "memory_size": 191,
#     "dtype": Int64Dtype(),
#     "types": {"int": 6, "float": 1},
#     "na_count": 1,
# }

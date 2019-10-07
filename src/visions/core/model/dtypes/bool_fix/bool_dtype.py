import pandas as pd
import numpy as np

from src.visions.core.model.dtypes.bool_fix.boolean import BoolDtype


series = pd.Series([1, 0, np.nan], dtype="Int8")
print(series)
print(series.dtype)
s2 = series.astype("Bool")
print(s2)
print(s2.dtype)

series = pd.Series([True, False])
print(series.astype("Bool"))

series = pd.Series([1, 2, 3, np.nan], dtype="Int8")
try:
    print(series.astype("Bool"))
except TypeError:
    print("Nice")
# Types have the most compact representation. All types are nullable.

# Bool
# Int8 when NaN
# Bool when bool

# Integer
# IntN when NaN
# int when int
# Float when inf

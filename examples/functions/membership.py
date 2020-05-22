import numpy as np
import pandas as pd

import visions as v

print(pd.Series([True, False]) in v.Boolean)  # True
print(pd.Series([True, False]) in v.Generic)  # True
print(pd.Series([True, False]) in v.Integer)  # False
print(pd.Series([True, False, np.nan]) in v.Boolean)  # False
print(pd.Series([True, False, None], dtype="Bool") in v.Boolean)  # True
print(pd.Series([True, False, np.nan]) in v.Object)  # True
print(pd.Series([True, False, np.nan], dtype="Bool") in v.Boolean)  # True

print(pd.Series([0, 1, 2, 3, np.nan], dtype="Int64") in v.Integer)  # True
print(pd.Series([0, 1, 2, 3], dtype=int) in v.Integer)  # True
print(pd.Series([0, 1, 2, 3], dtype="Int64") in v.Integer)  # True

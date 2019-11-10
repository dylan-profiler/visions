import pandas as pd
import numpy as np

from visions.core.implementations.types import (
    visions_bool,
    visions_generic,
    visions_integer,
    visions_object,
)

print(pd.Series([True, False]) in visions_bool)  # True
print(pd.Series([True, False]) in visions_generic)  # True
print(pd.Series([True, False]) in visions_integer)  # False
print(pd.Series([True, False, np.nan]) in visions_bool)  # False
print(pd.Series([True, False, None], dtype="Bool") in visions_bool)  # True
print(pd.Series([True, False, np.nan]) in visions_object)  # True
print(pd.Series([True, False, np.nan], dtype="Bool") in visions_bool)  # True

print(pd.Series([0, 1, 2, 3, np.nan], dtype="Int64") in visions_integer)  # True
print(pd.Series([0, 1, 2, 3], dtype=int) in visions_integer)  # True
print(pd.Series([0, 1, 2, 3], dtype="Int64") in visions_integer)  # True

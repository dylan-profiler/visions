import pandas as pd
import numpy as np

from tenzing.core.model.types import (
    tenzing_bool,
    tenzing_generic,
    tenzing_integer,
    missing_generic,
    tenzing_object,
)

print(pd.Series([True, False]) in tenzing_bool)  # True
print(pd.Series([True, False]) in tenzing_generic)  # True
print(pd.Series([True, False]) in tenzing_integer)  # False
print(pd.Series([True, False, np.nan]) in tenzing_bool)  # False
print(pd.Series([True, False, np.nan]) in tenzing_object)  # False
print(pd.Series([True, False, np.nan]) in missing_generic + tenzing_bool)  # True
print(pd.Series([True, False, np.nan]) in tenzing_bool + missing_generic)  # True
print(pd.Series([np.nan]) in missing_generic)  # True

print(pd.Series([0, 1, 2, 3, np.nan], dtype="Int64") in tenzing_integer)  # False
print(pd.Series([0, 1, 2, 3], dtype=int) in tenzing_integer + missing_generic)  # True
print(
    pd.Series([0, 1, 2, 3], dtype="Int64") in tenzing_integer + missing_generic
)  # True

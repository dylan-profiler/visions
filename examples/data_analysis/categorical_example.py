import pandas as pd

from visions.core import type_detect_series
from visions.core.implementations import visions_standard_set
from visions.core.implementations.types import visions_categorical, visions_bool

from examples.data_analysis.categorical import visions_category

ts = visions_standard_set()
ts -= visions_bool
ts -= visions_categorical
ts += visions_category

s1 = pd.Series(["A", "B", "C"] * 1000, dtype="category")
print(s1 in visions_category)
print(type_detect_series(s1, ts))

s2 = pd.Series([True, False] * 1000)
print(s2 in visions_category)
print(type_detect_series(s2, ts))

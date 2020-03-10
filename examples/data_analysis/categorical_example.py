import pandas as pd

from visions.functional import type_detect_series
from visions.typesets import standard_set
from visions.types import Categorical, Boolean

from examples.data_analysis.categorical import Category

ts = standard_set()
ts -= Boolean
ts -= Categorical
ts += Category

s1 = pd.Series(["A", "B", "C"] * 1000, dtype="category")
print(s1 in Category)
print(type_detect_series(s1, ts))

s2 = pd.Series([True, False] * 1000)
print(s2 in Category)
print(type_detect_series(s2, ts))

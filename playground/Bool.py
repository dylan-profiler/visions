import pandas as pd
import numpy as np
from pandas import Int8Dtype


@pd.api.extensions.register_extension_dtype
class Bool(Int8Dtype):
    name = "Bool"


x = pd.Series([True, False, False, np.nan] * 100000, dtype="Int8")
print(x.memory_usage(deep=True), x.dtype)

z = pd.Series([True, False, False, np.nan] * 100000)
print(z.memory_usage(deep=True), z.dtype)

y = pd.Series([True, False, False, False] * 100000, dtype="bool")
print(y.memory_usage(deep=True), y.dtype)

w = pd.Series([True, False, False, False] * 100000, dtype="Bool")
print(w.memory_usage(deep=True), w.dtype)
#

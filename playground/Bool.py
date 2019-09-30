import pandas as pd
import numpy as np
from pandas import Int8Dtype


@pd.api.extensions.register_extension_dtype
class Bool(Int8Dtype):
    name = "Bool"
    # TODO: overload dtype Int8 name...


x = pd.Series([True, False, False, np.nan] * 100000, dtype="Bool")
print(x.memory_usage(deep=True), x.dtype)

z = pd.Series([True, False, False, np.nan] * 100000)
print(z.memory_usage(deep=True), z.dtype)

u = pd.Series([True, False, False, np.nan] * 100000, dtype="float")
print(u.memory_usage(deep=True), u.dtype)

y = pd.Series([True, False, False, False] * 100000, dtype="bool")
print(y.memory_usage(deep=True), y.dtype)

w = pd.Series([True, False, False, False] * 100000, dtype="Bool")
print(w.memory_usage(deep=True), w.dtype)

v = u.astype("Bool")
print(v.memory_usage(deep=True), v.dtype)

# TODO: add object -> bool conversion or object -> float -> bool
t = z.astype(float).astype("Bool")
print(t.memory_usage(deep=True), t.dtype)

import pandas as pd
import pandas.api.types as pdt
import numpy as np

s = pd.Series([1, 2, 3, 100000000, np.nan], dtype="Int64")

print(s)

if not pdt.is_integer_dtype(s.dtype):
    raise ValueError("Nonono")

# For all nullable integers
types = ["UInt8", "Int8", "UInt16", "Int16", "UInt32", "Int32", "UInt64", "Int64"]
for np_type in types:
    info = np.iinfo(np_type)
    if s.min() >= info.min and s.max() <= info.max:
        print("conversion")
        s = s.astype(np_type)
        break

print(s)

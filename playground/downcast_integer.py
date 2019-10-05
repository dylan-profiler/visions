import pandas as pd
import numpy as np

s = pd.Series([1, 2, 3, 100000000])

print(s)

if not np.issubdtype(s.dtype, np.integer):
    raise ValueError("Nonono")

# For all integers
types = [
    np.uint8,
    np.int8,
    np.uint16,
    np.int16,
    np.uint32,
    np.int32,
    np.uint64,
    np.int64,
]
for np_type in types:
    info = np.iinfo(np_type)
    if s.min() >= info.min and s.max() <= info.max:
        print("conversion")
        s = s.astype(np_type)
        break

print(s)

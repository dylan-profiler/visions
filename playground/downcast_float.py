import pandas as pd
import numpy as np

s = pd.Series([1, 2, 3, 100000000, np.nan], dtype="float")

print(s)

# For all integers
types = [np.float16, np.float32, np.float64]
for np_type in types:
    info = np.finfo(np_type)
    if s.min() >= info.min and s.max() <= info.max:
        print("conversion")
        s = s.astype(np_type)
        break

print(s)

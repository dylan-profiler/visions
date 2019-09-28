import pandas as pd
import numpy as np
from pandas import Int8Dtype


@pd.api.extensions.register_extension_dtype
class Bool(Int8Dtype):
    name = "Bool"

    # @property
    # def type(self):
    #     return str
    # TODO: overload dtype Int8 name...
    # TODO: make sure True,False,np.nan, nothing else


series = pd.Series([complex(0, 1), np.nan], dtype=complex)
print(series)
print(series.dtype)

# Types have the most compact representation. All types are nullable.

# Bool
# Int8 when NaN
# Bool when bool

# Integer
# IntN when NaN
# int when int
# Float when inf


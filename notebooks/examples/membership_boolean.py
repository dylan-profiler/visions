import pandas as pd
import numpy as np

from tenzing.core.partitioners import MultiContainer, infinite, generic, missing, type
from tenzing.core.model.types.tenzing_bool import tenzing_bool

s1 = pd.Series([True, False], name="bool_series")
s2 = pd.Series([True, False, np.nan], name="bool_nan_series")
s3 = pd.Series([np.nan], name="nan_series")

for s in [s1, s2, s3]:
    print(f"**{s.name}**")
    print(s in tenzing_bool, "tenzing_bool")
    print(s in type[tenzing_bool], "type[tenzing_bool]")
    print(s in missing, "missing")
    print(
        s in MultiContainer([missing, type[tenzing_bool]]),
        "(missing)[type[tenzing_bool])",
    )
    print("")

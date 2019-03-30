import pandas as pd
import numpy as np
from tenzing.core.model_implementations import *


test_series = {
    tenzing_integer: pd.Series([0, 1, 2, 3, 4, np.nan]),
    tenzing_float: pd.Series([0.0, 1.0, 2.0, 3.0, 4.0, np.nan])
}


def infer_cast_type(series, values_out, type_in):
    if not (series in type_in):
        raise TypeError("Input series %s not of expected type %s!" % (series, type_in))

    inferred_type = type_in.infer_type(series)
    cast_series = inferred_type.cast_to_type(series)
    assert cast_series in inferred_type
    assert all(cast_series.values == values_out)

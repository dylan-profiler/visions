import pandas as pd
from pandas.api import types as pdt

from visions.backends.pandas.series_utils import (
    series_handle_nulls,
    series_not_empty,
    series_not_sparse,
)
from visions.types.object import Object

pandas_has_string_dtype_flag = hasattr(pdt, "is_string_dtype")


@Object.contains_op.register
@series_not_sparse
@series_handle_nulls
@series_not_empty
def object_contains(series: pd.Series, state: dict) -> bool:
    is_object = pdt.is_object_dtype(series)
    if is_object:
        ret = True
    elif pandas_has_string_dtype_flag:
        ret = pdt.is_string_dtype(series) and not pdt.is_categorical_dtype(series)
    else:
        ret = False
    return ret

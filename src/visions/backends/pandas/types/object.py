import pandas as pd
from pandas.api import types as pdt

from visions.backends.pandas.series_utils import series_not_empty, series_not_sparse
from visions.types.object import object_contains

pandas_has_string_dtype_flag = hasattr(pdt, "is_string_dtype")


@object_contains.register(pd.Series)
@series_not_sparse
@series_not_empty
def _(series: pd.Series, state: dict) -> bool:
    is_object = pdt.is_object_dtype(series)
    if is_object:
        ret = True
    elif pandas_has_string_dtype_flag:
        ret = pdt.is_string_dtype(series) and not pdt.is_categorical_dtype(series)
    else:
        ret = False
    return ret

import pandas as pd
from pandas.api import types as pdt

from visions.backends.pandas_be.series_utils import (
    series_handle_nulls,
    series_not_empty,
    series_not_sparse,
)
from visions.types.string import String

pandas_has_string_dtype_flag = hasattr(pdt, "is_string_dtype")


@series_handle_nulls
def _is_string(series: pd.Series, state: dict):
    return all(isinstance(v, str) for v in series)


@String.contains_op.register(pd.Series)
@series_not_sparse
@series_not_empty
def string_contains(series: pd.Series, state: dict) -> bool:
    # TODO: without the object check this passes string categories... is there a better way?
    if pdt.is_categorical_dtype(series):
        return False
    elif not pdt.is_object_dtype(series):
        return pandas_has_string_dtype_flag and pdt.is_string_dtype(series)

    return _is_string(series, state)

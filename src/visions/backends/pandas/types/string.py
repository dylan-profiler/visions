import pandas as pd
from pandas.api import types as pdt

from visions.backends.pandas.series_utils import (
    pandas_is_categorical,
    series_handle_nulls,
    series_not_empty,
    series_not_sparse,
)
from visions.types.string import String

pandas_has_string_dtype_flag = hasattr(pdt, "is_string_dtype")


@series_handle_nulls
def _is_string(series: pd.Series, state: dict):
    if isinstance(series.dtype, pd.SparseDtype):
        return pandas_sparse_is_string(series.array)

    if not all(isinstance(v, str) for v in series.values[0:5]):
        return False

    return (
        series.astype(str).to_numpy(dtype=object) == series.to_numpy(dtype=object)
    ).all()


def pandas_sparse_is_string(array: pd.arrays.SparseArray) -> bool:
    # Check if special values are not all strings
    if pandas_has_string_dtype_flag and not pdt.is_string_dtype(array.sp_values):
        return False

    # If every value is explicitly stored, fill_value is not semantic content
    if len(array) == len(array.sp_values):
        return True

    # Otherwise omitted positions are fill_value, so it must be string or missing
    return isinstance(array.fill_value, str) or pd.isna(array.fill_value)


@String.contains_op.register
@series_not_empty
def string_contains(series: pd.Series, state: dict) -> bool:
    if pandas_is_categorical(series):
        return False
    elif not pdt.is_object_dtype(series):
        return pandas_has_string_dtype_flag and pdt.is_string_dtype(series)

    return _is_string(series, state)

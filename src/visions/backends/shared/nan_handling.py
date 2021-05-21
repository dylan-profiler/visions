import numpy as np
import pandas as pd
from typing import Any
import math
from .utilities import has_import

has_numba = has_import("numba")

if has_numba:
    import numba as nb


_NANS = {None, np.nan}


def not_nan(v: Any) -> bool:
    return not pd.isna(v)


def nan_mask(array: np.ndarray) -> np.ndarray:
    # TODO: Fails for values like None, pandas resolves this but it's complicated some links:
    # https://github.com/pandas-dev/pandas/blob/3391a348f3f7cd07a96c8e6a4b05e3e9f60c8567/pandas/core/series.py#L192
    # https://github.com/pandas-dev/pandas/blob/65319af6e563ccbb02fb5152949957b6aef570ef/pandas/core/base.py#L816
    # https://github.com/pandas-dev/pandas/blob/65319af6e563ccbb02fb5152949957b6aef570ef/pandas/core/dtypes/missing.py#L133
    # https://github.com/pandas-dev/pandas/blob/65319af6e563ccbb02fb5152949957b6aef570ef/pandas/core/dtypes/missing.py#L202
    # raise NotImplementedError('Robust missing value detection not implemented for numpy arrays')
    try:
        mask = ~np.isnan(array)
    except TypeError:
        #mask = np.array([not pd. for v in array], dtype=bool)
        mask = ~pd.isna(array)
    return mask


if has_numba:

    @nb.jit
    def anynan(array: np.ndarray) -> bool:
        array = array.ravel()
        for i in range(array.size):
            if math.isnan(array[i]):
                return True
        return False


else:

    def anynan(array: np.ndarray) -> bool:
        return any(nan_check(v) for v in array)

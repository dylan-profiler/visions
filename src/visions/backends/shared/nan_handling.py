import math
from typing import Any, Iterator

import numpy as np
import pandas as pd

from .utilities import has_import

has_numba = has_import("numba")

if has_numba:
    import numba as nb


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
        # mask = np.array([not pd. for v in array], dtype=bool)
        mask = ~pd.isna(array)
    return mask


# TODO: There are optimizations here, just have to define precisely the desired missing ruleset in the
# generated jit
if has_numba:

    @nb.generated_jit(nopython=True)
    def is_missing(x):
        """
        Return True if the value is missing, False otherwise.
        """
        if isinstance(x, nb.types.Float):
            return lambda x: np.isnan(x)
        elif isinstance(x, (nb.types.NPDatetime, nb.types.NPTimedelta)):
            # The corresponding Not-a-Time value
            missing = x("NaT")
            return lambda x: x == missing
        elif x is None:
            return lambda x: True
        else:
            return lambda x: False

    @nb.jit
    def hasna(x: np.ndarray) -> bool:
        for item in x:
            if is_missing(item):
                return True
        return False


else:

    def anynan(array: np.ndarray) -> bool:
        return any(math.isnan(v) for v in array)

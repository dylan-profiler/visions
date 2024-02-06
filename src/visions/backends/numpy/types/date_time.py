from datetime import datetime
from functools import partial

import numpy as np
import pandas as pd

from visions.backends.numpy import test_utils
from visions.backends.numpy.array_utils import array_handle_nulls, array_not_empty
from visions.backends.pandas.types.date_time import pandas_infer_datetime
from visions.types import DateTime, String


@DateTime.register_relationship(String, np.ndarray)
@array_handle_nulls
def string_is_datetime(array: np.ndarray, state: dict) -> bool:
    exceptions = [OverflowError, TypeError]

    if len(array) == 0:
        return False

    coerced_array = test_utils.option_coercion_evaluator(
        partial(string_to_datetime, state=state), exceptions
    )(array)

    if coerced_array is None:
        return False
    elif np.isnat(coerced_array).any():
        return False

    return True


@DateTime.register_transformer(String, np.ndarray)
def string_to_datetime(array: np.ndarray, state: dict) -> np.ndarray:
    # return array.astype(np.datetime64)
    return pandas_infer_datetime(pd.Series(array), state).to_numpy()


@DateTime.contains_op.register
@array_handle_nulls
@array_not_empty
def datetime_contains(array: np.ndarray, state: dict) -> bool:
    if np.issubdtype(array.dtype, np.datetime64):
        return True

    return all(isinstance(v, datetime) for v in array)

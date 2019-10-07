import pandas as pd
import numpy as np
import pytest

from visions.core.dtypes.boolean import BoolDtype


@pytest.mark.parametrize(
    "series,expected_values,expected_dtype",
    [
        (pd.Series([True, False], dtype="Bool"), (True, False), "Bool"),
        (pd.Series([True, False], dtype=bool), (True, False), bool),
        (
            pd.Series([True, False, None, True, False, None], dtype="Bool"),
            (True, False, None, True, False, None),
            "Bool",
        ),
        (
            pd.Series([True, False, None, True, False, None], dtype=bool),
            (True, False, False, True, False, False),
            bool,
        ),
        (
            pd.Series([True, False, np.nan, True, False, np.nan], dtype="Bool"),
            (True, False, None, True, False, None),
            "Bool",
        ),
        (
            pd.Series([True, False, np.nan, True, False, np.nan], dtype=bool),
            (True, False, True, True, False, True),
            bool,
        ),
    ],
)
def test_series(series, expected_values, expected_dtype):
    value_series = pd.Series(expected_values)
    assert series[series.notna()].eq(value_series[value_series.notna()]).all()
    assert series.dtype == expected_dtype

import numpy as np
import pandas as pd
import pytest


@pytest.mark.parametrize(
    "series,expected_values,expected_dtype",
    [
        (pd.Series([True, False], dtype="boolean"), (True, False), "boolean"),
        (pd.Series([True, False], dtype=bool), (True, False), bool),
        (
            pd.Series([True, False, None, True, False, None], dtype="boolean"),
            (True, False, None, True, False, None),
            "boolean",
        ),
        (
            pd.Series([True, False, None, True, False, None], dtype=bool),
            (True, False, False, True, False, False),
            bool,
        ),
        (
            pd.Series([True, False, np.nan, True, False, np.nan], dtype="boolean"),
            (True, False, None, True, False, None),
            "boolean",
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

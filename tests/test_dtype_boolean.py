import numpy as np
import pandas as pd
import pytest

from visions.types.boolean import hasnan_bool_name


@pytest.mark.parametrize(
    "series,expected_values,expected_dtype",
    [
        (
            pd.Series([True, False], dtype=hasnan_bool_name),
            (True, False),
            hasnan_bool_name,
        ),
        (pd.Series([True, False], dtype=bool), (True, False), bool),
        (
            pd.Series([True, False, None, True, False, None], dtype=hasnan_bool_name),
            (True, False, None, True, False, None),
            hasnan_bool_name,
        ),
        (
            pd.Series([True, False, None, True, False, None], dtype=bool),
            (True, False, False, True, False, False),
            bool,
        ),
        (
            pd.Series(
                [True, False, np.nan, True, False, np.nan], dtype=hasnan_bool_name
            ),
            (True, False, None, True, False, None),
            hasnan_bool_name,
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

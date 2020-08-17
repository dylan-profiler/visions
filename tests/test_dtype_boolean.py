import numpy as np
import pandas as pd
import pytest


if int(pd.__version__.split(".")[0]) >= 1:
    type_name = "boolean"
else:
    from visions.dtypes.boolean import BoolDtype

    type_name = "Bool"


@pytest.mark.parametrize(
    "series,expected_values,expected_dtype",
    [
        (pd.Series([True, False], dtype=type_name), (True, False), type_name),
        (pd.Series([True, False], dtype=bool), (True, False), bool),
        (
            pd.Series([True, False, None, True, False, None], dtype=type_name),
            (True, False, None, True, False, None),
            type_name,
        ),
        (
            pd.Series([True, False, None, True, False, None], dtype=bool),
            (True, False, False, True, False, False),
            bool,
        ),
        (
            pd.Series([True, False, np.nan, True, False, np.nan], dtype=type_name),
            (True, False, None, True, False, None),
            type_name,
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

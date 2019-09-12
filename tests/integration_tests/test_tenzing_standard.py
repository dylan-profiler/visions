import pandas as pd
import numpy as np
from shapely import wkt
import pytest

from tenzing.core.model_implementations.typesets import tenzing_standard


_test_suite = [
    pd.Series([1, 2, 3], name="int_series"),
    pd.Series([1, 2, 3], name="categorical_int_series", dtype="category"),
    pd.Series([1, 2, np.nan], name="int_nan_series"),
    pd.Series([1.0, 2.1, 3.0], name="float_series"),
    pd.Series([1.0, 2.5, np.nan], name="float_nan_series"),
    pd.Series([1.0, 2.0, 3.1], dtype="category", name="categorical_float_series"),
    pd.Series(["hello", "world"], name="string_series"),
    pd.Series(["hello", "world"], dtype="category", name="categorical_string_series"),
    pd.Series(["2017-10-01", "12/05/2017"], name="timestamp_string_series"),
    pd.Series([True, False], name="bool_series"),
    pd.Series(
        [np.complex(0, 0), np.complex(1, 2), np.complex(3, -1), np.nan],
        name="complex_series",
    ),
    pd.Series(
        [np.complex(0, 0), np.complex(1, 2), np.complex(3, -1), np.nan],
        name="categorical_complex_series",
        dtype="category",
    ),
    pd.Series(
        [pd.datetime(2017, 3, 5), pd.datetime(2019, 12, 4)], name="timestamp_series"
    ),
    pd.Series(
        ["POINT (-92 42)", "POINT (-92 42.1)", "POINT (-92 42.2)"],
        name="geometry_string_series",
    ),
    pd.Series(
        [
            wkt.loads("POINT (-92 42)"),
            wkt.loads("POINT (-92 42.1)"),
            wkt.loads("POINT (-92 42.2)"),
        ],
        name="geometry_series",
    ),
]


@pytest.fixture(params=_test_suite, ids=lambda series: series.name)
def test_series(request):
    yield request.param


@pytest.fixture(params=_test_suite, ids=lambda series: series.name)
def test_tenzing_standard(series):
    pass

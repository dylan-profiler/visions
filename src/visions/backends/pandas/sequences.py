import datetime
from typing import Dict, Iterable

import numpy as np
import pandas as pd

from visions.backends.pandas.test_utils import pandas_version
from visions.backends.pandas.types.boolean import hasnan_bool_name


def get_sequences() -> Dict[str, Iterable]:
    sequences = {
        "float_series6": pd.Series([np.nan, 1.1], dtype=np.single),
        "bool_series2": pd.Series([True, False, False, True], dtype=bool),
        "nullable_bool_series": pd.Series([True, False, None], dtype=hasnan_bool_name),
        "int_str_range": pd.Series(range(20)).astype("str"),
        "Int64_int_series": pd.Series([1, 2, 3], dtype="Int64"),
        "Int64_int_nan_series": pd.Series([1, 2, 3, np.nan], dtype="Int64"),
        "pd_uint32": pd.Series([1, 2, 3, 4], dtype="UInt32"),
        "categorical_int_series": pd.Series([1, 2, 3], dtype="category"),
        "categorical_char": pd.Series(
            pd.Categorical(
                ["A", "B", "C", "C", "B", "A"],
                categories=["A", "B", "C"],
                ordered=False,
            ),
        ),
        "categorical_float_series": pd.Series([1.0, 2.0, 3.1], dtype="category"),
        "categorical_string_series": pd.Series(["Georgia", "Sam"], dtype="category"),
        "categorical_complex_series": pd.Series(
            [np.complex(0, 0), np.complex(1, 2), np.complex(3, -1)],
            dtype="category",
        ),
        "ordinal": pd.Series(
            pd.Categorical(
                ["A", "B", "C", "C", "B", "A"],
                categories=["A", "B", "C"],
                ordered=True,
            ),
        ),
        "timestamp_series": pd.to_datetime(
            pd.Series(
                [
                    datetime.datetime(2017, 3, 5, 12, 2),
                    datetime.datetime(2019, 12, 4),
                ],
            )
        ),
        "timestamp_series_nat": pd.to_datetime(
            pd.Series(
                [
                    datetime.datetime(2017, 3, 5),
                    datetime.datetime(2019, 12, 4, 3, 2, 0),
                    pd.NaT,
                ],
            )
        ),
        "date_series_nat": pd.to_datetime(
            pd.Series(
                [
                    datetime.datetime(2017, 3, 5),
                    datetime.datetime(2019, 12, 4),
                    pd.NaT,
                ],
            )
        ),
        "timestamp_aware_series": pd.Series(
            pd.date_range(
                start="2013-05-18 12:00:01",
                periods=2,
                freq="H",
                tz="Europe/Brussels",
            )
        ),
        "datetime": pd.to_datetime(
            pd.Series(
                [
                    datetime.date(2011, 1, 1),
                    datetime.date(2012, 1, 2),
                    datetime.date(2013, 1, 1),
                ],
            )
        ),
        # http://pandas-docs.github.io/pandas-docs-travis/user_guide/timeseries.html#timestamp-limitations
        # pd.to_datetime(
        #     pd.Series(
        #         [
        #             datetime.datetime(year=1, month=1, day=1, hour=8, minute=43, second=12),
        #             datetime.datetime(year=1, month=1, day=1, hour=9, minute=43, second=12),
        #             datetime.datetime(
        #                 year=1, month=1, day=1, hour=10, minute=43, second=12
        #             ),
        #         ],
        #         name="datetime_to_time",
        #     )
        # ),
        "timedelta_series": pd.Series([pd.Timedelta(days=i) for i in range(3)]),
        "timedelta_series_nat": pd.Series(
            [pd.Timedelta(days=i) for i in range(3)] + [pd.NaT],
        ),
        "timedelta_negative": pd.Series(
            [
                pd.Timedelta("1 days 00:03:43"),
                pd.Timedelta("5 days 12:33:57"),
                pd.Timedelta("0 days 01:25:07"),
                pd.Timedelta("-2 days 13:46:56"),
                pd.Timedelta("1 days 23:49:25"),
            ],
        ),
        "empty_float": pd.Series([], dtype=float),
        "empty_int64": pd.Series([], dtype="Int64"),
        "empty_object": pd.Series([], dtype="object"),
        "empty_bool": pd.Series([], dtype=bool),
        "float_series4": pd.Series([1, 2, 3.05, 4], dtype=np.float),
        # Null Sequences
        "all_null_none": pd.Series([None, None]),
        "all_null_nan": pd.Series([np.nan, np.nan]),
        "all_null_nat": pd.Series([pd.NaT, pd.NaT]),
        "all_null_empty_str": pd.Series(["", ""]),
    }

    if pandas_version[0] >= 1:
        sequences["string_dtype_series"] = pd.Series(
            ["Patty", "Valentine"], dtype="string"
        )

    return sequences

import datetime
import os
import pathlib
import uuid
from ipaddress import IPv4Address, IPv6Address
from pathlib import PurePosixPath, PureWindowsPath
from urllib.parse import urlparse

import numpy as np
import pandas as pd

from visions.types.email_address import FQDA

base_path = os.path.abspath(os.path.dirname(__file__))


def get_series():
    test_series = [
        # Int Series
        pd.Series([1, 2, 3], name="int_series"),
        pd.Series(range(10), name="int_range"),
        pd.Series([1, 2, 3], name="Int64_int_series", dtype="Int64"),
        pd.Series([1, 2, 3, np.nan], name="Int64_int_nan_series", dtype="Int64"),
        pd.Series([1, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0], name="int_series_boolean"),
        # Count
        pd.Series(np.array([1, 2, 3, 4], dtype=np.uint32), name="np_uint32"),
        pd.Series(np.array([1, 2, 3, 4], dtype="UInt32"), name="pd_uint32"),
        # Categorical
        pd.Series([1, 2, 3], name="categorical_int_series", dtype="category"),
        pd.Series(
            pd.Categorical(
                ["A", "B", "C", "C", "B", "A"],
                categories=["A", "B", "C"],
                ordered=False,
            ),
            name="categorical_char",
        ),
        pd.Series([1.0, 2.0, 3.1], dtype="category", name="categorical_float_series"),
        pd.Series(
            ["Georgia", "Sam"], dtype="category", name="categorical_string_series"
        ),
        pd.Series(
            [np.complex(0, 0), np.complex(1, 2), np.complex(3, -1)],
            name="categorical_complex_series",
            dtype="category",
        ),
        # Ordinal
        pd.Series(
            pd.Categorical(
                ["A", "B", "C", "C", "B", "A"], categories=["A", "B", "C"], ordered=True
            ),
            name="ordinal",
        ),
        # Float Series
        pd.Series([1.0, 2.1, 3.0], name="float_series"),
        pd.Series([1.0, 2.5, np.nan], name="float_nan_series"),
        pd.Series([1.0, 2.0, 3.0, 4.0], name="float_series2"),
        pd.Series(np.array([1.2, 2, 3, 4], dtype=np.float), name="float_series3"),
        pd.Series([1, 2, 3.05, 4], dtype=np.float, name="float_series4"),
        pd.Series([np.nan, 1.2], name="float_series5"),
        pd.Series([np.nan, 1.1], dtype=np.single, name="float_series6"),
        pd.Series([np.inf, np.NINF, np.PINF, 1000000.0, 5.5], name="float_with_inf"),
        pd.Series([np.inf, np.NINF, np.Infinity, np.PINF], name="inf_series"),
        pd.Series([1, 2, np.nan], name="int_nan_series"),
        # Nan Series
        pd.Series([np.nan], name="nan_series"),
        pd.Series([np.nan, np.nan, np.nan, np.nan], name="nan_series_2"),
        # String Series
        pd.Series(["Patty", "Valentine"], name="string_series"),
        pd.Series(["mack", "the", "finger"], name="string_unicode_series"),
        pd.Series(
            np.array(["upper", "hall"], dtype=np.unicode_),
            name="string_np_unicode_series",
        ),
        pd.Series(["1.0", "2.0", np.nan], name="string_num_nan"),
        pd.Series(["1,000.0", "2.1", np.nan], name="string_with_sep_num_nan"),
        pd.Series(["1.0", "2.0", "3.0"], name="string_num"),
        pd.Series(["1.0", "45.67", np.nan], name="string_flt_nan"),
        pd.Series(["1.0", "45.67", "3.5"], name="string_flt"),
        pd.Series(
            [
                "I was only robbing the register,",
                "I hope you understand",
                "One of us had better call up the cops",
                "In the hot New Jersey night",
                np.nan,
            ],
            name="string_str_nan",
        ),
        pd.Series(["True", "False", None], name="string_bool_nan"),
        pd.Series(range(20), name="int_str_range").astype("str"),
        pd.Series(
            [
                "http://www.cwi.nl:80/%7Eguido/Python.html",
                "https://github.com/dylan-profiling/hurricane",
            ],
            name="str_url",
        ),
        pd.Series(
            [r"C:\\home\\user\\file.txt", r"C:\\home\\user\\test2.txt"],
            name="path_series_windows_str",
        ),
        pd.Series(
            [r"/home/user/file.txt", r"/home/user/test2.txt"],
            name="path_series_linux_str",
        ),
        pd.Series(["0011", "12"], name="str_int_leading_zeros"),
        pd.Series(["0.0", "0.04", "0"], name="str_float_non_leading_zeros"),
        pd.Series(["0.0", "0.000", "0", "2"], name="str_int_zeros"),
        # Bool Series
        pd.Series([True, False], name="bool_series"),
        pd.Series([True, False, None], name="bool_nan_series"),
        pd.Series([True, False, None], name="nullable_bool_series", dtype="Bool"),
        pd.Series([True, False, False, True], name="bool_series2", dtype=bool),
        pd.Series([True, False, False, True], name="bool_series2", dtype=bool),
        pd.Series(np.array([1, 0, 0, 1], dtype=np.bool), name="bool_series3"),
        # Complex Series
        pd.Series(
            [np.complex(0, 0), np.complex(1, 2), np.complex(3, -1)],
            name="complex_series",
        ),
        pd.Series(
            [
                np.complex(0, 0),
                np.complex(1, 2),
                np.complex(3, -1),
                np.complex(np.nan, np.nan),
            ],
            name="complex_series_nan",
        ),
        pd.Series(["(1+1j)", "(2+2j)", "(10+100j)"], name="str_complex"),
        pd.Series(["(1+1j)", "(2+2j)", "(10+100j)", "NaN"], name="str_complex_nan"),
        pd.Series(
            [np.complex(0, 0), np.complex(1, 2), np.complex(3, -1), np.nan],
            name="complex_series_nan_2",
        ),
        pd.Series(
            [complex(0, 0), complex(1, 2), complex(3, -1), np.nan],
            name="complex_series_py_nan",
        ),
        pd.Series(
            [complex(0, 0), complex(1, 2), complex(3, -1)], name="complex_series_py"
        ),
        pd.Series(
            [np.complex(0, 0), np.complex(1, 0), np.complex(3, 0), np.complex(-1, 0)],
            name="complex_series_float",
        ),
        # Datetime Series
        pd.Series(["1937-05-06", "20/4/2014"], name="string_date"),
        pd.Series(["1941-05-24", "13/10/2016"], name="timestamp_string_series"),
        pd.to_datetime(
            pd.Series(
                [datetime.datetime(2017, 3, 5, 12, 2), datetime.datetime(2019, 12, 4)],
                name="timestamp_series",
            )
        ),
        pd.to_datetime(
            pd.Series(
                [
                    datetime.datetime(2017, 3, 5),
                    datetime.datetime(2019, 12, 4, 3, 2, 0),
                    pd.NaT,
                ],
                name="timestamp_series_nat",
            )
        ),
        pd.to_datetime(
            pd.Series(
                [datetime.datetime(2017, 3, 5), datetime.datetime(2019, 12, 4), pd.NaT],
                name="date_series_nat",
            )
        ),
        pd.Series(
            pd.date_range(
                start="2013-05-18 12:00:01",
                periods=2,
                freq="H",
                tz="Europe/Brussels",
                name="timestamp_aware_series",
            )
        ),
        pd.to_datetime(
            pd.Series(
                [
                    datetime.date(2011, 1, 1),
                    datetime.date(2012, 1, 2),
                    datetime.date(2013, 1, 1),
                ],
                name="datetime",
            )
        ),
        # Date series
        pd.Series(
            [
                datetime.date(2011, 1, 1),
                datetime.date(2012, 1, 2),
                datetime.date(2013, 1, 1),
            ],
            name="date",
        ),
        # Time series
        pd.Series(
            [
                datetime.time(8, 43, 12),
                datetime.time(9, 43, 12),
                datetime.time(10, 43, 12),
            ],
            name="time",
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
        # Timedelta Series
        pd.Series([pd.Timedelta(days=i) for i in range(3)], name="timedelta_series"),
        pd.Series(
            [pd.Timedelta(days=i) for i in range(3)] + [pd.NaT],
            name="timedelta_series_nat",
        ),
        pd.Series(
            [
                pd.Timedelta("1 days 00:03:43"),
                pd.Timedelta("5 days 12:33:57"),
                pd.Timedelta("0 days 01:25:07"),
                pd.Timedelta("-2 days 13:46:56"),
                pd.Timedelta("1 days 23:49:25"),
            ],
            name="timedelta_negative",
        ),
        # Path Series
        pd.Series(
            [
                PurePosixPath("/home/user/file.txt"),
                PurePosixPath("/home/user/test2.txt"),
            ],
            name="path_series_linux",
        ),
        pd.Series(
            [
                PurePosixPath("/home/user/file.txt"),
                PurePosixPath("/home/user/test2.txt"),
                None,
            ],
            name="path_series_linux_missing",
        ),
        pd.Series(
            [
                PureWindowsPath("C:\\home\\user\\file.txt"),
                PureWindowsPath("C:\\home\\user\\test2.txt"),
            ],
            name="path_series_windows",
        ),
        # Url Series
        pd.Series(
            [
                urlparse("http://www.cwi.nl:80/%7Eguido/Python.html"),
                urlparse("https://github.com/dylan-profiling/hurricane"),
            ],
            name="url_series",
        ),
        pd.Series(
            [
                urlparse("http://www.cwi.nl:80/%7Eguido/Python.html"),
                urlparse("https://github.com/dylan-profiling/hurricane"),
                np.nan,
            ],
            name="url_nan_series",
        ),
        pd.Series(
            [
                urlparse("http://www.cwi.nl:80/%7Eguido/Python.html"),
                urlparse("https://github.com/dylan-profiling/hurricane"),
                None,
            ],
            name="url_none_series",
        ),
        # UUID Series
        pd.Series(
            [
                uuid.UUID("0b8a22ca-80ad-4df5-85ac-fa49c44b7ede"),
                uuid.UUID("aaa381d6-8442-4f63-88c8-7c900e9a23c6"),
                uuid.UUID("00000000-0000-0000-0000-000000000000"),
            ],
            name="uuid_series",
        ),
        pd.Series(
            [
                uuid.UUID("0b8a22ca-80ad-4df5-85ac-fa49c44b7ede"),
                uuid.UUID("aaa381d6-8442-4f63-88c8-7c900e9a23c6"),
                uuid.UUID("00000000-0000-0000-0000-000000000000"),
                None,
            ],
            name="uuid_series_missing",
        ),
        pd.Series(
            [
                "0b8a22ca-80ad-4df5-85ac-fa49c44b7ede",
                "aaa381d6-8442-4f63-88c8-7c900e9a23c6",
                "00000000-0000-0000-0000-000000000000",
            ],
            name="uuid_series_str",
        ),
        # Object Series
        pd.Series([[1, ""], [2, "Rubin"], [3, "Carter"]], name="mixed_list[str,int]"),
        pd.Series(
            [{"why": "did you"}, {"bring him": "in for he"}, {"aint": "the guy"}],
            name="mixed_dict",
        ),
        pd.Series(
            [pd.to_datetime, pd.to_timedelta, pd.read_json, pd.to_pickle],
            name="callable",
        ),
        pd.Series([pd, np], name="module"),
        pd.Series(["1.1", "2"], name="textual_float"),
        pd.Series(["1.1", "2", "NAN"], name="textual_float_nan"),
        # Object (Mixed, https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.api.types.infer_dtype.html)
        pd.Series(["a", 1], name="mixed_integer"),
        pd.Series([True, False, np.nan], name="mixed"),
        pd.Series([[True], [False], [False]], name="mixed_list"),
        pd.Series([[1, ""], [2, "Rubin"], [3, "Carter"]], name="mixed_list[str,int]"),
        pd.Series(
            [{"why": "did you"}, {"bring him": "in for he"}, {"aint": "the guy"}],
            name="mixed_dict",
        ),
        # IP
        pd.Series([IPv4Address("127.0.0.1"), IPv4Address("127.0.0.1")], name="ip"),
        pd.Series(["127.0.0.1", "127.0.0.1"], name="ip_str"),
        # Empty
        pd.Series([], name="empty"),
        pd.Series([], name="empty_float", dtype=float),
        pd.Series([], name="empty_int64", dtype="Int64"),
        pd.Series([], name="empty_object", dtype="object"),
        pd.Series([], name="empty_bool", dtype=bool),
        # All null series
        pd.Series([None, None], name="all_null_none"),
        pd.Series([np.nan, np.nan], name="all_null_nan"),
        pd.Series([pd.NaT, pd.NaT], name="all_null_nat"),
        pd.Series(["", ""], name="all_null_empty_str"),
        # IP
        pd.Series([IPv4Address("127.0.0.1"), IPv4Address("127.0.0.1")], name="ip"),
        pd.Series(
            [IPv4Address("127.0.0.1"), None, IPv4Address("127.0.0.1")],
            name="ip_missing",
        ),
        pd.Series(
            [IPv6Address("0:0:0:0:0:0:0:1"), IPv4Address("127.0.0.1")],
            name="ip_mixed_v4andv6",
        ),
        pd.Series(["127.0.0.1", "127.0.0.1"], name="ip_str"),
        # File
        pd.Series(
            [
                pathlib.Path(os.path.join(base_path, "series.py")).absolute(),
                pathlib.Path(os.path.join(base_path, "__init__.py")).absolute(),
                pathlib.Path(os.path.join(base_path, "utils.py")).absolute(),
            ],
            name="file_test_py",
        ),
        pd.Series(
            [
                pathlib.Path(os.path.join(base_path, "..", "py.typed")).absolute(),
                pathlib.Path(
                    os.path.join(
                        base_path, "..", "visualisation", "circular_packing.html"
                    )
                ).absolute(),
                pathlib.Path(os.path.join(base_path, "series.py")).absolute(),
            ],
            name="file_mixed_ext",
        ),
        pd.Series(
            [
                pathlib.Path(os.path.join(base_path, "series.py")).absolute(),
                None,
                pathlib.Path(os.path.join(base_path, "__init__.py")).absolute(),
                None,
                pathlib.Path(os.path.join(base_path, "utils.py")).absolute(),
            ],
            name="file_test_py_missing",
        ),
        # Image
        pd.Series(
            [
                pathlib.Path(
                    os.path.join(
                        base_path,
                        "../visualisation/typesets/typeset_complete.png",
                    )
                ).absolute(),
                pathlib.Path(
                    os.path.join(
                        base_path,
                        r"../visualisation/typesets/typeset_standard.png",
                    )
                ).absolute(),
                pathlib.Path(
                    os.path.join(
                        base_path,
                        r"../visualisation/typesets/typeset_geometry.png",
                    )
                ).absolute(),
            ],
            name="image_png",
        ),
        pd.Series(
            [
                pathlib.Path(
                    os.path.join(
                        base_path,
                        r"../visualisation/typesets/typeset_complete.png",
                    )
                ).absolute(),
                pathlib.Path(
                    os.path.join(
                        base_path,
                        r"../visualisation/typesets/typeset_standard.png",
                    )
                ).absolute(),
                None,
                pathlib.Path(
                    os.path.join(
                        base_path,
                        r"../visualisation/typesets/typeset_geometry.png",
                    )
                ).absolute(),
                None,
            ],
            name="image_png_missing",
        ),
        # Email
        pd.Series(
            [FQDA("test", "example.com"), FQDA("info", "example.eu")],
            name="email_address",
        ),
        pd.Series(
            [FQDA("test", "example.com"), FQDA("info", "example.eu"), None],
            name="email_address_missing",
        ),
        pd.Series(["test@example.com", "info@example.eu"], name="email_address_str"),
    ]

    if int(pd.__version__.split(".")[0]) >= 1:
        pandas_1_series = [
            pd.Series(
                ["Patty", "Valentine"], dtype="string", name="string_dtype_series"
            )
        ]
        test_series.extend(pandas_1_series)

    return test_series

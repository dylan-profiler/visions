import datetime
import os
import pathlib
import uuid
from ipaddress import IPv4Address, IPv6Address
from pathlib import PurePosixPath, PureWindowsPath
from typing import Dict, Iterable, List
from urllib.parse import urlparse

import numpy as np
import pandas as pd

from visions.types.email_address import FQDA

base_path = os.path.abspath(os.path.dirname(__file__))


# python
# iterator:     list, set, tuple, iter
# element:      int, float, complex
# missing:      None
# dtype:        ?

# numpy
# iterator:     array
# element:      np.inf, -np.inf
# missing:      np.nan
# dtype:        np.int, np.complex, np.float, np.single

# pandas
# iterator:     Series, Categorical
# element:
# missing:      pd.NA, pd.NAT
# dtype:        "Int64", "UInt32", "category"


def get_sequences() -> Dict[str, Iterable]:
    sequences = {
        "int_series": [1, 2, 3],
        "int_range": range(10),
        "int_series_boolean": [1, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0],
        "float_series": [1.0, 2.1, 3.0],
        "float_series2": [1.0, 2.0, 3.0, 4.0],
        "string_series": ["Patty", "Valentine"],
        "string_unicode_series": ["mack", "the", "finger"],
        "string_num": ["1.0", "2.0", "3.0"],
        "string_flt": ["1.0", "45.67", "3.5"],
        "string_bool_nan": ["True", "False", None],
        "str_url": [
            "http://www.cwi.nl:80/%7Eguido/Python.html",
            "https://github.com/dylan-profiling/hurricane",
        ],
        "path_series_windows_str": [
            r"C:\\home\\user\\file.txt",
            r"C:\\home\\user\\test2.txt",
        ],
        "path_series_linux_str": [r"/home/user/file.txt", r"/home/user/test2.txt"],
        "str_int_leading_zeros": ["0011", "12"],
        "str_float_non_leading_zeros": ["0.0", "0.04", "0"],
        "str_int_zeros": ["0.0", "0.000", "0", "2"],
        "bool_series": [True, False],
        "bool_nan_series": [True, False, None],
        "str_complex": ["(1+1j)", "(2+2j)", "(10+100j)"],
        "str_complex_nan": ["(1+1j)", "(2+2j)", "(10+100j)", "NaN"],
        "complex_series_py": [complex(0, 0), complex(1, 2), complex(3, -1)],
        "complex_series_py_float": [complex(0, 0), complex(1, 0), complex(3, 0)],
        "string_date": ["1937-05-06", "20/4/2014"],
        "timestamp_string_series": ["1941-05-24", "13/10/2016"],
        "date": [
            datetime.date(2011, 1, 1),
            datetime.date(2012, 1, 2),
            datetime.date(2013, 1, 1),
        ],
        "time": [
            datetime.time(8, 43, 12),
            datetime.time(9, 43, 12),
            datetime.time(10, 43, 12),
        ],
        "path_series_linux": [
            PurePosixPath("/home/user/file.txt"),
            PurePosixPath("/home/user/test2.txt"),
        ],
        "path_series_linux_missing": [
            PurePosixPath("/home/user/file.txt"),
            PurePosixPath("/home/user/test2.txt"),
            None,
        ],
        "path_series_windows": [
            PureWindowsPath("C:\\home\\user\\file.txt"),
            PureWindowsPath("C:\\home\\user\\test2.txt"),
        ],
        "url_series": [
            urlparse("http://www.cwi.nl:80/%7Eguido/Python.html"),
            urlparse("https://github.com/dylan-profiling/hurricane"),
        ],
        "url_none_series": [
            urlparse("http://www.cwi.nl:80/%7Eguido/Python.html"),
            urlparse("https://github.com/dylan-profiling/hurricane"),
            None,
        ],
        "uuid_series": [
            uuid.UUID("0b8a22ca-80ad-4df5-85ac-fa49c44b7ede"),
            uuid.UUID("aaa381d6-8442-4f63-88c8-7c900e9a23c6"),
            uuid.UUID("00000000-0000-0000-0000-000000000000"),
        ],
        "uuid_series_missing": [
            uuid.UUID("0b8a22ca-80ad-4df5-85ac-fa49c44b7ede"),
            uuid.UUID("aaa381d6-8442-4f63-88c8-7c900e9a23c6"),
            uuid.UUID("00000000-0000-0000-0000-000000000000"),
            None,
        ],
        "uuid_series_str": [
            "0b8a22ca-80ad-4df5-85ac-fa49c44b7ede",
            "aaa381d6-8442-4f63-88c8-7c900e9a23c6",
            "00000000-0000-0000-0000-000000000000",
        ],
        "mixed_list[str,int]": [[1, ""], [2, "Rubin"], [3, "Carter"]],
        "mixed_dict": [
            {"why": "did you"},
            {"bring him": "in for he"},
            {"aint": "the guy"},
        ],
        "callable": [os.getcwd, os.stat, os.kill],
        "module": [os, uuid],
        "textual_float": ["1.1", "2"],
        "textual_float_nan": ["1.1", "2", "NAN"],
        "mixed_integer": ["a", 1],
        "mixed_list": [[True], [False], [False]],
        "ip_str": ["127.0.0.1", "127.0.0.1"],
        "empty": [],
        "ip": [IPv4Address("127.0.0.1"), IPv4Address("127.0.0.1")],
        "ip_missing": [IPv4Address("127.0.0.1"), None, IPv4Address("127.0.0.1")],
        "ip_mixed_v4andv6": [IPv6Address("0:0:0:0:0:0:0:1"), IPv4Address("127.0.0.1")],
        "file_test_py": [
            pathlib.Path(os.path.join(base_path, "series.py")).absolute(),
            pathlib.Path(os.path.join(base_path, "__init__.py")).absolute(),
            pathlib.Path(os.path.join(base_path, "utils.py")).absolute(),
        ],
        "file_mixed_ext": [
            pathlib.Path(os.path.join(base_path, "..", "py.typed")).absolute(),
            pathlib.Path(
                os.path.join(base_path, "..", "visualisation", "circular_packing.html")
            ).absolute(),
            pathlib.Path(os.path.join(base_path, "series.py")).absolute(),
        ],
        "file_test_py_missing": [
            pathlib.Path(os.path.join(base_path, "series.py")).absolute(),
            None,
            pathlib.Path(os.path.join(base_path, "__init__.py")).absolute(),
            None,
            pathlib.Path(os.path.join(base_path, "utils.py")).absolute(),
        ],
        "image_png": [
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
        "image_png_missing": [
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
        "email_address": [FQDA("test", "example.com"), FQDA("info", "example.eu")],
        "email_address_missing": [
            FQDA("test", "example.com"),
            FQDA("info", "example.eu"),
            None,
        ],
        "email_address_str": ["test@example.com", "info@example.eu"],
    }
    return sequences


def get_series() -> Dict[str, pd.Series]:
    sequences = get_sequences()

    test_series = {name: pd.Series(sequence) for name, sequence in sequences.items()}

    test_series.update(
        {
            # Numpy-specific
            "complex_series_float": pd.Series(
                [
                    np.complex(0, 0),
                    np.complex(1, 0),
                    np.complex(3, 0),
                    np.complex(-1, 0),
                ],
            ),
            "url_nan_series": pd.Series(
                [
                    urlparse("http://www.cwi.nl:80/%7Eguido/Python.html"),
                    urlparse("https://github.com/dylan-profiling/hurricane"),
                    np.nan,
                ],
            ),
            "mixed": pd.Series([True, False, np.nan]),
            "float_series3": pd.Series(np.array([1.2, 2, 3, 4], dtype=np.float)),
            "float_series4": pd.Series([1, 2, 3.05, 4], dtype=np.float),
            "np_uint32": pd.Series(np.array([1, 2, 3, 4], dtype=np.uint32)),
            "float_nan_series": pd.Series([1.0, 2.5, np.nan]),
            "float_series5": pd.Series([np.nan, 1.2]),
            "float_series6": pd.Series([np.nan, 1.1], dtype=np.single),
            "float_with_inf": pd.Series([np.inf, np.NINF, np.PINF, 1000000.0, 5.5]),
            "inf_series": pd.Series([np.inf, np.NINF, np.Infinity, np.PINF]),
            "int_nan_series": pd.Series([1, 2, np.nan]),
            "nan_series": pd.Series([np.nan]),
            "nan_series_2": pd.Series([np.nan, np.nan, np.nan, np.nan]),
            "string_np_unicode_series": pd.Series(
                np.array(["upper", "hall"], dtype=np.unicode_),
            ),
            "string_num_nan": pd.Series(["1.0", "2.0", np.nan]),
            "string_with_sep_num_nan": pd.Series(["1,000.0", "2.1", np.nan]),
            "string_flt_nan": pd.Series(["1.0", "45.67", np.nan]),
            "string_str_nan": [
                "I was only robbing the register,",
                "I hope you understand",
                "One of us had better call up the cops",
                "In the hot New Jersey night",
                np.nan,
            ],
            "bool_series3": pd.Series(np.array([1, 0, 0, 1], dtype=np.bool)),
            "complex_series": [np.complex(0, 0), np.complex(1, 2), np.complex(3, -1)],
            "complex_series_nan": [
                np.complex(0, 0),
                np.complex(1, 2),
                np.complex(3, -1),
                np.complex(np.nan, np.nan),
            ],
            "complex_series_nan_2": [
                np.complex(0, 0),
                np.complex(1, 2),
                np.complex(3, -1),
                np.nan,
            ],
            "complex_series_py_nan": [
                complex(0, 0),
                complex(1, 2),
                complex(3, -1),
                np.nan,
            ],
            # Pandas-specific
            "bool_series2": pd.Series([True, False, False, True], dtype=bool),
            "nullable_bool_series": pd.Series([True, False, None], dtype="Bool"),
            "int_str_range": pd.Series(range(20)).astype("str"),
            "Int64_int_series": pd.Series([1, 2, 3], dtype="Int64"),
            "Int64_int_nan_series": pd.Series([1, 2, 3, np.nan], dtype="Int64"),
            "pd_uint32": pd.Series(np.array([1, 2, 3, 4], dtype="UInt32")),
            "categorical_int_series": pd.Series([1, 2, 3], dtype="category"),
            "categorical_char": pd.Series(
                pd.Categorical(
                    ["A", "B", "C", "C", "B", "A"],
                    categories=["A", "B", "C"],
                    ordered=False,
                ),
            ),
            "categorical_float_series": pd.Series([1.0, 2.0, 3.1], dtype="category"),
            "categorical_string_series": pd.Series(
                ["Georgia", "Sam"], dtype="category"
            ),
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
        }
    )

    if int(pd.__version__.split(".")[0]) >= 1:
        pandas_1_series = pd.Series(["Patty", "Valentine"], dtype="string")
        test_series["string_dtype_series"] = pandas_1_series

    return test_series

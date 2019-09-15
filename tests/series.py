import datetime
from pathlib import PureWindowsPath, PurePosixPath
from urllib.parse import urlparse
import pandas as pd
import numpy as np
from shapely import wkt


def get_series():
    return [
        # Int Series
        pd.Series([1, 2, 3], name="int_series"),
        pd.Series([1, 2, 3], name="categorical_int_series", dtype="category"),
        pd.Series([1, 2, np.nan], name="int_nan_series"),
        pd.Series([1, 2, 3], name="Int64_int_series", dtype="Int64"),
        pd.Series([1, 2, 3, np.nan], name="Int64_int_nan_series", dtype="Int64"),
        pd.Series(np.array([1, 2, 3, 4], dtype=np.uint32), name="np_uint32"),
        pd.Series([np.inf, np.NINF, np.PINF, 1000000.0, 5.0], name="int_with_inf"),
        pd.Series(range(10), name="int_range"),
        # Float Series
        pd.Series([1.0, 2.1, 3.0], name="float_series"),
        pd.Series([1.0, 2.5, np.nan], name="float_nan_series"),
        pd.Series([1.1, 2, 3, 4], name="float_series2"),
        pd.Series(np.array([1.2, 2, 3, 4], dtype=np.float), name="float_series3"),
        pd.Series([1, 2, 3.05, 4], dtype=float, name="float_series4"),
        pd.Series([np.nan, 1.2], name="float_series5"),
        pd.Series([np.nan, 1.1], dtype=np.single, name="float_series6"),
        pd.Series([1.0, 2.0, 3.1], dtype="category", name="categorical_float_series"),
        pd.Series([np.inf, np.NINF, np.PINF, 1000000.0, 5.5], name="float_with_inf"),
        # String Series
        pd.Series(["Patty", "Valentine"], name="string_series"),
        pd.Series(
            ["Georgia", "Sam"], dtype="category", name="categorical_string_series"
        ),
        pd.Series(["1941-05-24", "13/10/2016"], name="timestamp_string_series"),
        pd.Series(["mack", "the", "finger"], name="string_unicode_series"),
        pd.Series(
            np.array(["upper", "hall"], dtype=np.unicode_),
            name="string_np_unicode_series",
        ),
        pd.Series(["1.0", "2.0", np.nan], name="string_num_nan"),
        pd.Series(["1.0", "45.67", np.nan], name="string_flt_nan"),
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
        pd.Series(["True", "False", np.nan], name="string_bool_nan"),
        pd.Series(range(20), name="int_str_range").astype("str"),
        pd.Series(["1937-05-06", "20/4/2014"], name="string_date"),
        # Bool Series
        pd.Series([True, False], name="bool_series"),
        pd.Series([True, False, np.nan], name="bool_nan_series"),
        pd.Series([True, False, False, True], dtype=bool, name="bool_series2"),
        pd.Series(np.array([1, 0, 0, 1], dtype=np.bool), name="bool_series3"),
        # Complex Series
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
            [complex(0, 0), complex(1, 2), complex(3, -1), np.nan],
            name="complex_series_py_nan",
        ),
        pd.Series(
            [complex(0, 0), complex(1, 2), complex(3, -1)], name="complex_series_py"
        ),
        # Datetime Series
        pd.Series(
            [pd.datetime(2017, 3, 5), pd.datetime(2019, 12, 4)], name="timestamp_series"
        ),
        pd.Series(
            [pd.datetime(2017, 3, 5), pd.datetime(2019, 12, 4), pd.NaT],
            name="timestamp_series_nat",
        ),
        pd.date_range(
            start="2013-05-18 12:00:00",
            periods=2,
            freq="H",
            tz="Europe/Brussels",
            name="timestamp_aware_series",
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
        # Timedelta Series
        pd.Series([pd.Timedelta(days=i) for i in range(3)], name="timedelta_series"),
        pd.Series(
            [pd.Timedelta(days=i) for i in range(3)] + [pd.NaT],
            name="timedelta_series_nat",
        ),
        # Geometry Series
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
        # Path Series
        pd.Series(
            [
                PurePosixPath("/home/user/file.txt"),
                PurePosixPath("/home/user/test2.txt"),
            ],
            name="path_series_linux",
        ),
        pd.Series(
            [r"/home/user/file.txt", r"/home/user/test2.txt"],
            name="path_series_linux_str",
        ),
        pd.Series(
            [
                PureWindowsPath("C:\\home\\user\\file.txt"),
                PureWindowsPath("C:\\home\\user\\test2.txt"),
            ],
            name="path_series_windows",
        ),
        pd.Series(
            [r"C:\\home\\user\\file.txt", r"C:\\home\\user\\test2.txt"],
            name="path_series_windows_str",
        ),
        # Url Series
        pd.Series(
            [
                urlparse("http://www.cwi.nl:80/%7Eguido/Python.html"),
                urlparse("https://github.com/dylan-profiling/hurricane"),
            ],
            name="url_series",
        ),
        # Object Series
        pd.Series([[1, ""], [2, "Rubin"], [3, "Carter"]], name="mixed_list[str,int]"),
        pd.Series(
            [{"why": "did you"}, {"bring him": "in for he"}, {"aint": "the guy"}],
            name="mixed_dict",
        ),
        # ?
        pd.Series([None, None, None, None, None], name="none_series"),
        pd.Series(
            [pd.to_datetime, pd.to_timedelta, pd.read_json, pd.to_pickle],
            name="callable",
        ),
        pd.Series([pd, wkt, np], name="module"),
        pd.Series(["1.1", "2"], name="textual_float"),
        pd.Series(["1.1", "2", "NAN", "N/A"], name="textual_float_nan"),
        # Empty
        pd.Series([], name="empty"),
        pd.Series([], name="empty_float", dtype=float),
        pd.Series([], name="empty_int64", dtype="Int64"),
        pd.Series([], name="empty_object", dtype="object"),
        pd.Series([], name="empty_bool", dtype=bool),
    ]

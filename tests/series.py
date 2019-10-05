import datetime
from ipaddress import IPv4Address
from pathlib import PureWindowsPath, PurePosixPath
from urllib.parse import urlparse
import pandas as pd
import numpy as np
from shapely import wkt

from tenzing.core.model.types import *


def get_series():
    return [
        # Int Series
        pd.Series([1, 2, 3], name="int_series"),
        pd.Series(range(10), name="int_range"),
        pd.Series([1, 2, 3], name="Int64_int_series", dtype="Int64"),
        pd.Series([1, 2, 3, np.nan], name="Int64_int_nan_series", dtype="Int64"),
        # Count
        pd.Series(np.array([1, 2, 3, 4], dtype=np.uint32), name="np_uint32"),
        # Categorical
        pd.Series([1, 2, 3], name="categorical_int_series", dtype="category"),
        pd.Series(pd.Categorical(['A', 'B', 'C', 'C', 'B', 'A'], categories=['A', 'B', 'C'], ordered=False),
                  name='categorical_char'),
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
        pd.Series(pd.Categorical(['A', 'B', 'C', 'C', 'B', 'A'], categories=['A', 'B', 'C'], ordered=True), name='ordinal'),
        # Float Series
        pd.Series([1.0, 2.1, 3.0], name="float_series"),
        pd.Series([1.0, 2.5, np.nan], name="float_nan_series"),
        pd.Series([1.0, 2.0, 3.0, 4.0], name="float_series2"),
        pd.Series(np.array([1.2, 2, 3, 4], dtype=np.float), name="float_series3"),
        pd.Series([1, 2, 3.05, 4], dtype=float, name="float_series4"),
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
        pd.Series(["1941-05-24", "13/10/2016"], name="timestamp_string_series"),
        pd.Series(["mack", "the", "finger"], name="string_unicode_series"),
        pd.Series(
            np.array(["upper", "hall"], dtype=np.unicode_),
            name="string_np_unicode_series",
        ),
        pd.Series(["1.0", "2.0", np.nan], name="string_num_nan"),
        pd.Series(["1.0", "2.0", "3.0"], name="string_num"),
        pd.Series(["1.0", "45.67", np.nan], name="string_flt_nan"),
        pd.Series(["1.0", "45.67", "3.5"], name="string_flt"),
        pd.Series(
            ["POINT (-92 42)", "POINT (-92 42.1)", "POINT (-92 42.2)"],
            name="geometry_string_series",
        ),
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
        pd.Series(
            [
                "http://www.cwi.nl:80/%7Eguido/Python.html",
                "https://github.com/pandas-profiling/pandas-profiling",
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
        # Bool Series
        pd.Series([True, False], name="bool_series"),
        pd.Series([True, False, np.nan], name="bool_nan_series"),
        # pd.Series([True, False, np.nan], name='nullable_bool_series', dtype='Bool'),
        pd.Series([True, False, False, True], dtype=bool, name="bool_series2"),
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
        # Datetime Series
        pd.Series(
            [pd.datetime(2017, 3, 5, 12, 2), pd.datetime(2019, 12, 4)],
            name="timestamp_series",
        ),
        pd.Series(
            [pd.datetime(2017, 3, 5), pd.datetime(2019, 12, 4, 3, 2, 0), pd.NaT],
            name="timestamp_series_nat",
        ),
        pd.Series(
            [pd.datetime(2017, 3, 5), pd.datetime(2019, 12, 4), pd.NaT],
            name="date_series_nat",
        ),
        pd.Series(
            pd.date_range(
                start="2013-05-18 12:00:00",
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
        # Timedelta Series
        pd.Series([pd.Timedelta(days=i) for i in range(3)], name="timedelta_series"),
        pd.Series(
            [pd.Timedelta(days=i) for i in range(3)] + [pd.NaT],
            name="timedelta_series_nat",
        ),
        # Geometry Series
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
        pd.Series([pd, wkt, np], name="module"),
        pd.Series(["1.1", "2"], name="textual_float"),
        pd.Series(["1.1", "2", "NAN"], name="textual_float_nan"),
        # Empty
        pd.Series([], name="empty"),
        pd.Series([], name="empty_float", dtype=float),
        pd.Series([], name="empty_int64", dtype="Int64"),
        pd.Series([], name="empty_object", dtype="object"),
        pd.Series([], name="empty_bool", dtype=bool),
        # IP
        pd.Series([IPv4Address("127.0.0.1"), IPv4Address("127.0.0.1")], name="ip"),
        pd.Series(["127.0.0.1", "127.0.0.1"], name="ip_str"),
    ]


def get_contains_map():
    series_map = {
        tenzing_integer: [
            "int_series",
            "Int64_int_series",
            "int_range",
            "Int64_int_nan_series",
        ],
        tenzing_count: [
            "np_uint32",
        ],
        tenzing_path: ["path_series_linux", "path_series_windows"],
        tenzing_url: ["url_series"],
        tenzing_float: [
            "float_series",
            "float_series2",
            "float_series3",
            "float_series4",
            "inf_series",
            "nan_series",
            "float_nan_series",
            "float_series5",
            "int_nan_series",
            "nan_series_2",
            "float_with_inf",
            "float_series6",
        ],
        tenzing_categorical: [
            "categorical_int_series",
            "categorical_float_series",
            "categorical_string_series",
            "categorical_complex_series",
            'categorical_char',
            'ordinal'
        ],
        tenzing_bool: [
            "bool_series",
            "bool_series2",
            "bool_series3",
            # "nullable_bool_series",
        ],
        tenzing_complex: [
            "complex_series",
            "complex_series_py",
            "complex_series_nan",
            "complex_series_py_nan",
            "complex_series_nan_2",
        ],
        tenzing_datetime: [
            "timestamp_series",
            "timestamp_aware_series",
            "datetime",
            "timestamp_series_nat",
            "date_series_nat",
        ],
        tenzing_date: ["datetime", "date_series_nat"],
        tenzing_timedelta: ["timedelta_series", "timedelta_series_nat"],
        tenzing_string: [
            "timestamp_string_series",
            "string_series",
            "geometry_string_series",
            "string_unicode_series",
            "string_np_unicode_series",
            "path_series_linux_str",
            "path_series_windows_str",
            "int_str_range",
            "string_date",
            "textual_float",
            "textual_float_nan",
            "ip_str",
            "string_flt",
            "string_num",
            "str_url",
            "string_str_nan",
            "string_num_nan",
            "string_bool_nan",
            "string_flt_nan",
        ],
        tenzing_geometry: ["geometry_series"],
        tenzing_ip: ["ip"],
        tenzing_ordinal: ['ordinal']
    }

    series_map[tenzing_object] = (
        ["mixed_list[str,int]", "mixed_dict", "callable", "module", "bool_nan_series"]
        + series_map[tenzing_string]
        + series_map[tenzing_geometry]
        + series_map[tenzing_path]
        + series_map[tenzing_url]
        + series_map[tenzing_ip]
    )

    # TODO: Series with missing and Inf values

    # Empty series
    all = ["empty", "empty_bool", "empty_float", "empty_int64", "empty_object"]
    for key, values in series_map.items():
        all += values
    series_map[tenzing_generic] = list(set(all))

    return series_map


def infer_series_type_map():
    return {
        "int_series": tenzing_integer,
        "categorical_int_series": tenzing_categorical,
        "int_nan_series": tenzing_integer,
        "Int64_int_series": tenzing_integer,
        "Int64_int_nan_series": tenzing_integer,
        "np_uint32": tenzing_count,
        "int_range": tenzing_integer,
        "float_series": tenzing_float,
        "float_nan_series": tenzing_float,
        "float_series2": tenzing_integer,
        "float_series3": tenzing_float,
        "float_series4": tenzing_float,
        "float_series5": tenzing_float,
        "float_series6": tenzing_float,
        "categorical_float_series": tenzing_categorical,
        "float_with_inf": tenzing_float,
        "inf_series": tenzing_float,
        "nan_series": tenzing_float,
        "nan_series_2": tenzing_float,
        "string_series": tenzing_string,
        "categorical_string_series": tenzing_categorical,
        "timestamp_string_series": tenzing_date,
        "string_unicode_series": tenzing_string,
        "string_np_unicode_series": tenzing_string,
        "string_num_nan": tenzing_integer,
        "string_num": tenzing_integer,
        "string_flt_nan": tenzing_float,
        "string_flt": tenzing_float,
        "string_str_nan": tenzing_string,
        "string_bool_nan": tenzing_bool,
        "int_str_range": tenzing_integer,
        "string_date": tenzing_date,
        "str_url": tenzing_url,
        "bool_series": tenzing_bool,
        "bool_nan_series": tenzing_bool,
        # "nullable_bool_series": tenzing_bool,
        "bool_series2": tenzing_bool,
        "bool_series3": tenzing_bool,
        "complex_series": tenzing_complex,
        "complex_series_nan": tenzing_complex,
        "complex_series_nan_2": tenzing_complex,
        "complex_series_py_nan": tenzing_complex,
        "complex_series_py": tenzing_complex,
        "categorical_complex_series": tenzing_categorical,
        "timestamp_series": tenzing_datetime,
        "timestamp_series_nat": tenzing_datetime,
        "timestamp_aware_series": tenzing_datetime,
        "datetime": tenzing_date,
        "timedelta_series": tenzing_timedelta,
        "timedelta_series_nat": tenzing_timedelta,
        "geometry_string_series": tenzing_geometry,
        "geometry_series": tenzing_geometry,
        "path_series_linux": tenzing_path,
        "path_series_linux_str": tenzing_path,
        "path_series_windows": tenzing_path,
        "path_series_windows_str": tenzing_path,
        "url_series": tenzing_url,
        "mixed_list[str,int]": tenzing_object,
        "mixed_dict": tenzing_object,
        "callable": tenzing_object,
        "module": tenzing_object,
        "textual_float": tenzing_float,
        "textual_float_nan": tenzing_float,
        "empty": tenzing_generic,
        "empty_object": tenzing_generic,
        "empty_float": tenzing_generic,
        "empty_bool": tenzing_generic,
        "empty_int64": tenzing_generic,
        "ip": tenzing_ip,
        "ip_str": tenzing_ip,
        "date_series_nat": tenzing_date,
        "categorical_char": tenzing_categorical,
        'ordinal': tenzing_ordinal,
    }


def get_convert_map():
    series_map = [
        # Model type, Relation type
        (tenzing_integer, tenzing_float, []),
        (tenzing_integer, tenzing_string, ["string_num", "int_str_range", "string_num_nan"]),
        (
            tenzing_float,
            tenzing_string,
            [
                "string_flt",
                "string_num_nan",
                "string_flt",
                "string_flt_nan",
                "textual_float",
                "textual_float_nan"
            ],
        ),
        (tenzing_datetime, tenzing_string, ["timestamp_string_series", "string_date"]),
        (tenzing_geometry, tenzing_string, ["geometry_string_series"]),
        (tenzing_bool, tenzing_string, ["string_bool_nan"]),
        (tenzing_ip, tenzing_string, ["ip_str"]),
        (tenzing_url, tenzing_string, ["str_url"]),
        (tenzing_path, tenzing_string, ["path_series_windows_str", "path_series_linux_str"]),
        # (tenzing_bool, tenzing_object, ["bool_nan_series"])
    ]

    return series_map

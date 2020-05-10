import datetime
import uuid
from ipaddress import IPv4Address
from pathlib import PureWindowsPath, PurePosixPath
from urllib.parse import urlparse
import pandas as pd
import numpy as np
from shapely import wkt

from visions.types import (
    Boolean,
    Categorical,
    Complex,
    Count,
    Date,
    DateTime,
    File,
    Float,
    Generic,
    Geometry,
    Image,
    Integer,
    IPAddress,
    Object,
    Ordinal,
    Path,
    String,
    Time,
    TimeDelta,
    URL,
    UUID,
)


def get_series():
    return [
        # Int Series
        pd.Series([1, 2, 3], name="int_series"),
        pd.Series(range(10), name="int_range"),
        pd.Series([1, 2, 3], name="Int64_int_series", dtype="Int64"),
        pd.Series([1, 2, 3, np.nan], name="Int64_int_nan_series", dtype="Int64"),
        pd.Series([1, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0], name="int_series_boolean"),
        # Count
        pd.Series(np.array([1, 2, 3, 4], dtype=np.uint32), name="np_uint32"),
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
        pd.Series(["1941-05-24", "13/10/2016"], name="timestamp_string_series"),
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
        pd.Series(["True", "False", None], name="string_bool_nan"),
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
        pd.Series([True, False, None], name="bool_nan_series"),
        pd.Series([True, False, None], name="nullable_bool_series", dtype="Bool"),
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
        pd.Series(["(1+1j)", "(2+2j)", "(10+100j)"], name="str_complex"),
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
        pd.Series(
            [datetime.datetime(2017, 3, 5, 12, 2), datetime.datetime(2019, 12, 4)],
            name="timestamp_series",
        ),
        pd.Series(
            [
                datetime.datetime(2017, 3, 5),
                datetime.datetime(2019, 12, 4, 3, 2, 0),
                pd.NaT,
            ],
            name="timestamp_series_nat",
        ),
        pd.Series(
            [datetime.datetime(2017, 3, 5), datetime.datetime(2019, 12, 4), pd.NaT],
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
        pd.Series(
            [
                urlparse("http://www.cwi.nl:80/%7Eguido/Python.html"),
                urlparse("https://github.com/dylan-profiling/hurricane"),
                np.nan,
            ],
            name="url_nan_series",
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
        Integer: [
            "int_series",
            "Int64_int_series",
            "int_range",
            "Int64_int_nan_series",
            "int_series_boolean",
        ],
        Count: ["np_uint32"],
        Path: ["path_series_linux", "path_series_windows"],
        URL: ["url_series", "url_nan_series"],
        Float: [
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
        Categorical: [
            "categorical_int_series",
            "categorical_float_series",
            "categorical_string_series",
            "categorical_complex_series",
            "categorical_char",
            "ordinal",
        ],
        Boolean: [
            "bool_series",
            "bool_series2",
            "bool_series3",
            "nullable_bool_series",
        ],
        Complex: [
            "complex_series",
            "complex_series_py",
            "complex_series_nan",
            "complex_series_py_nan",
            "complex_series_nan_2",
            "complex_series_float",
        ],
        DateTime: [
            "timestamp_series",
            "timestamp_aware_series",
            "datetime",
            "timestamp_series_nat",
            "date_series_nat",
        ],
        Date: ["datetime", "date_series_nat"],
        TimeDelta: ["timedelta_series", "timedelta_series_nat"],
        String: [
            "timestamp_string_series",
            "string_with_sep_num_nan",
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
            "str_complex",
            "uuid_series_str",
        ],
        Geometry: ["geometry_series"],
        IPAddress: ["ip"],
        Ordinal: ["ordinal"],
        UUID: ["uuid_series"],
    }

    series_map[Object] = (
        ["mixed_list[str,int]", "mixed_dict", "callable", "module", "bool_nan_series"]
        + series_map[String]
        + series_map[Geometry]
        + series_map[Path]
        + series_map[URL]
        + series_map[IPAddress]
        + series_map[UUID]
    )

    # Empty series
    all = ["empty", "empty_bool", "empty_float", "empty_int64", "empty_object"]
    for key, values in series_map.items():
        all += values
    series_map[Generic] = list(set(all))

    return series_map


def infer_series_type_map():
    return {
        "int_series": Integer,
        "categorical_int_series": Categorical,
        "int_nan_series": Integer,
        "Int64_int_series": Integer,
        "Int64_int_nan_series": Integer,
        "np_uint32": Count,
        "int_range": Integer,
        "float_series": Float,
        "float_nan_series": Float,
        "int_series_boolean": Boolean,
        "float_series2": Integer,
        "float_series3": Float,
        "float_series4": Float,
        "float_series5": Float,
        "float_series6": Float,
        "complex_series_float": Integer,
        "categorical_float_series": Categorical,
        "float_with_inf": Float,
        "inf_series": Float,
        "nan_series": Float,
        "nan_series_2": Float,
        "string_series": String,
        "categorical_string_series": Categorical,
        "timestamp_string_series": Date,
        "string_with_sep_num_nan": String,  # TODO: Introduce thousands separator
        "string_unicode_series": String,
        "string_np_unicode_series": String,
        "string_num_nan": Integer,
        "string_num": Integer,
        "string_flt_nan": Float,
        "string_flt": Float,
        "string_str_nan": String,
        "string_bool_nan": Boolean,
        "int_str_range": Integer,
        "string_date": Date,
        "str_url": URL,
        "bool_series": Boolean,
        "bool_nan_series": Boolean,
        "nullable_bool_series": Boolean,
        "bool_series2": Boolean,
        "bool_series3": Boolean,
        "complex_series": Complex,
        "complex_series_nan": Complex,
        "complex_series_nan_2": Complex,
        "complex_series_py_nan": Complex,
        "complex_series_py": Complex,
        "categorical_complex_series": Categorical,
        "timestamp_series": DateTime,
        "timestamp_series_nat": DateTime,
        "timestamp_aware_series": DateTime,
        "datetime": Date,
        "timedelta_series": TimeDelta,
        "timedelta_series_nat": TimeDelta,
        "geometry_string_series": Geometry,
        "geometry_series": Geometry,
        "path_series_linux": Path,
        "path_series_linux_str": Path,
        "path_series_windows": Path,
        "path_series_windows_str": Path,
        "url_series": URL,
        "url_nan_series": URL,
        "mixed_list[str,int]": Object,
        "mixed_dict": Object,
        "callable": Object,
        "module": Object,
        "textual_float": Float,
        "textual_float_nan": Float,
        "empty": Generic,
        "empty_object": Generic,
        "empty_float": Generic,
        "empty_bool": Generic,
        "empty_int64": Generic,
        "ip": IPAddress,
        "ip_str": IPAddress,
        "date_series_nat": Date,
        "categorical_char": Categorical,
        "ordinal": Ordinal,
        "str_complex": Complex,
        "uuid_series": UUID,
        "uuid_series_str": UUID,
    }


def get_convert_map():
    # Conversions in one single step
    series_map = [
        # Model type, Relation type
        (Integer, Float, ["int_nan_series", "float_series2"]),
        (Complex, String, ["str_complex"]),
        (
            Float,
            String,
            [
                "string_flt",
                "string_num_nan",
                "string_num",
                "string_flt_nan",
                "textual_float",
                "textual_float_nan",
                "int_str_range",
                # "string_with_sep_num_nan",
            ],
        ),
        (DateTime, String, ["timestamp_string_series", "string_date"]),
        (Geometry, String, ["geometry_string_series"]),
        (Boolean, String, ["string_bool_nan"]),
        (IPAddress, String, ["ip_str"]),
        (URL, String, ["str_url"]),
        (Path, String, ["path_series_windows_str", "path_series_linux_str"]),
        (Float, Complex, ["complex_series_float"]),
        (Boolean, Integer, ["int_series_boolean"]),
        (Boolean, Object, ["bool_nan_series"]),
        (UUID, String, ["uuid_series_str"]),
    ]

    return series_map

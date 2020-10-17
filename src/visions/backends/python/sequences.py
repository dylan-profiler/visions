import datetime
import os
import uuid
from ipaddress import IPv4Address, IPv6Address
from pathlib import Path, PurePosixPath, PureWindowsPath
from typing import Dict, Sequence, cast
from urllib.parse import urlparse

from visions.types.email_address import FQDA


def get_sequences() -> Dict[str, Sequence]:
    base_path = Path(__file__).parent.parent.parent.absolute()

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
        "py_datetime_str": ["1941-05-24 00:05:00", "2016-10-13 00:10:00"],
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
            Path(os.path.join(base_path, "test/series.py")).absolute(),
            Path(os.path.join(base_path, "test/__init__.py")).absolute(),
            Path(os.path.join(base_path, "test/utils.py")).absolute(),
        ],
        "file_mixed_ext": [
            Path(os.path.join(base_path, "py.typed")).absolute(),
            Path(os.path.join(base_path, "test/data", "file.html")).absolute(),
            Path(os.path.join(base_path, "test/series.py")).absolute(),
        ],
        "file_test_py_missing": [
            Path(os.path.join(base_path, "test/series.py")).absolute(),
            None,
            Path(os.path.join(base_path, "test/__init__.py")).absolute(),
            None,
            Path(os.path.join(base_path, "test/utils.py")).absolute(),
        ],
        "image_png": [
            Path(
                os.path.join(
                    base_path,
                    "test/data",
                    "img.png",
                )
            ).absolute(),
            Path(
                os.path.join(
                    base_path,
                    "test/data",
                    "img.jpeg",
                )
            ).absolute(),
            Path(
                os.path.join(
                    base_path,
                    "test/data",
                    "img.jpg",
                )
            ).absolute(),
        ],
        "image_png_missing": [
            Path(
                os.path.join(
                    base_path,
                    "test/data",
                    "img.png",
                )
            ).absolute(),
            Path(
                os.path.join(
                    base_path,
                    "test/data",
                    "img.jpeg",
                )
            ).absolute(),
            None,
            Path(
                os.path.join(
                    base_path,
                    "test/data",
                    "img.jpg",
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
    assert all(isinstance(v, Sequence) for v in sequences.values())
    return cast(Dict[str, Sequence], sequences)

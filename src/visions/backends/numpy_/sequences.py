from typing import Dict, Sequence
from urllib.parse import urlparse

import numpy as np


def get_sequences() -> Dict[str, Sequence]:
    sequences = {
        "complex_series_float": [
            np.complex(0, 0),
            np.complex(1, 0),
            np.complex(3, 0),
            np.complex(-1, 0),
        ],
        "url_nan_series": [
            urlparse("http://www.cwi.nl:80/%7Eguido/Python.html"),
            urlparse("https://github.com/dylan-profiling/hurricane"),
            np.nan,
        ],
        "mixed": [True, False, np.nan],
        "float_nan_series": [1.0, 2.5, np.nan],
        "float_series5": [np.nan, 1.2],
        "float_with_inf": [np.inf, np.NINF, np.PINF, 1000000.0, 5.5],
        "inf_series": [np.inf, np.NINF, np.Infinity, np.PINF],
        "int_nan_series": [1, 2, np.nan],
        "nan_series": [np.nan],
        "nan_series_2": [np.nan, np.nan, np.nan, np.nan],
        "string_num_nan": ["1.0", "2.0", np.nan],
        "string_with_sep_num_nan": ["1,000.0", "2.1", np.nan],
        "string_flt_nan": ["1.0", "45.67", np.nan],
        "string_str_nan": [
            "I was only robbing the register,",
            "I hope you understand",
            "One of us had better call up the cops",
            "In the hot New Jersey night",
            np.nan,
        ],
        "float_series3": np.array([1.2, 2, 3, 4], dtype=np.float),
        "np_uint32": np.array([1, 2, 3, 4], dtype=np.uint32),
        "string_np_unicode_series": np.array(["upper", "hall"], dtype=np.unicode_),
        "complex_series": [np.complex(0, 0), np.complex(1, 2), np.complex(3, -1)],
        "bool_series3": np.array([1, 0, 0, 1], dtype=np.bool),
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
    }
    return sequences

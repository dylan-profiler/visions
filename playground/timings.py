import pandas as pd
from pathlib import PurePosixPath

from visions.core.implementations import visions_complete_set
from visions.core.functional import type_cast, type_inference

n_elems = 1000000

df = pd.DataFrame(
    {
        "ip_str": ["127.0.0.1"] * n_elems,
        "float_str": ["1.1", "NAN"] * int(n_elems / 2),
        "obj_series": [[1, ""]] * n_elems,
        "path": [PurePosixPath("/home/user/file.txt")] * n_elems,
        "integer": [3] * n_elems,
        "bool_int": [1, 0] * int(n_elems / 2),
        "string_date": ["1937-05-06"] * n_elems,
    }
)

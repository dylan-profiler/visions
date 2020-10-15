from typing import Dict

import numpy as np
import pandas as pd

from visions.backends.pandas.test_utils import pandas_version

not_pandas_1_0_5 = not (
    (pandas_version[0] == 1) and (pandas_version[1] == 0) and (pandas_version[2] == 5)
)


def get_sparse_series() -> Dict[str, pd.Series]:
    test_series = {
        "int_sparse": pd.Series([-1, 0, 1, 2, 3], dtype=pd.SparseDtype(np.int32, 0)),
        "float_sparse": pd.Series(
            [np.nan, 0, 1, 2, 3],
            dtype=pd.SparseDtype(np.float64, np.nan),
        ),
        "complex_sparse": pd.Series(
            [np.nan, complex(0, 1), complex(1, -1), complex(2, 4), complex(3, -12)],
            dtype=pd.SparseDtype(np.complex128, np.nan),
        ),
        "bool_sparse": pd.Series(
            [True, False, False],
            dtype=pd.SparseDtype(np.bool, False),
        ),
        "str_obj_sparse": pd.Series(
            pd.arrays.SparseArray([None, None, "gold", "black", "silver"]),
        ),
        # Pending https://github.com/pandas-dev/pandas/issues/35762
        # pd.Series([NoneT, 0, 1, 2, 3, 4], name="datetime_sparse", dtype=pd.SparseDtype(np.datetime64)),
        # Pandas dtypes
        "pd_int64_sparse": pd.Series(
            [0, 1, 2, 3, None],
            dtype=pd.SparseDtype(pd.Int64Dtype()),
        ),
        # Pending https://github.com/pandas-dev/pandas/issues/35793
        # pd.Series(
        #     ["a", "b", "c", None],
        #     name="pd_categorical_sparse",
        #     dtype=pd.SparseDtype(pd.CategoricalDtype(['a', 'b', 'c', 'd']))
        # )
    }

    if pandas_version[0] >= 1 and not_pandas_1_0_5:
        test_series["pd_string_sparse"] = pd.Series(
            ["Patty", "Valentine", "Upper", "", "", ""],
            dtype=pd.SparseDtype(pd.StringDtype(), ""),
        )
        test_series["pd_bool_sparse"] = pd.Series(
            [True, False, False, None],
            dtype=pd.SparseDtype(pd.BooleanDtype(), None),
        )

    return test_series

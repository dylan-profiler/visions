import numpy as np
import pandas as pd


def get_sparse_series():
    test_series = [
        # Numpy dtypes
        pd.Series(
            [-1, 0, 1, 2, 3], name="int_sparse", dtype=pd.SparseDtype(np.int32, 0)
        ),
        pd.Series(
            [np.nan, 0, 1, 2, 3],
            name="float_sparse",
            dtype=pd.SparseDtype(np.float64, np.nan),
        ),
        pd.Series(
            [np.nan, complex(0, 1), complex(1, -1), complex(2, 4), complex(3, -12)],
            name="complex_sparse",
            dtype=pd.SparseDtype(np.complex128, np.nan),
        ),
        pd.Series(
            [True, False, False],
            name="bool_sparse",
            dtype=pd.SparseDtype(np.bool, False),
        ),
        pd.Series(
            [pd.NA, pd.NA, "gold", "black", "silver"],
            name="str_obj_sparse",
            dtype=pd.SparseDtype(np.object, pd.NA),
        ),
        # Pending https://github.com/pandas-dev/pandas/issues/35762
        # pd.Series([pd.NaT, 0, 1, 2, 3, 4], name="datetime_sparse", dtype=pd.SparseDtype(np.datetime64)),
        # Pandas dtypes
        pd.Series(
            [True, False, False, pd.NA],
            name="pd_bool_sparse",
            dtype=pd.SparseDtype(pd.BooleanDtype(), pd.NA),
        ),
        pd.Series(
            [0, 1, 2, 3, None],
            name="pd_int64_sparse",
            dtype=pd.SparseDtype(pd.Int64Dtype()),
        ),
    ]
    return test_series

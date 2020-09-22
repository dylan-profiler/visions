import numpy as np
import pandas as pd

nan_value = pd.NA if hasattr(pd, "NA") else None


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
            pd.arrays.SparseArray([None, None, "gold", "black", "silver"]),
            name="str_obj_sparse",
        ),
        # Pending https://github.com/pandas-dev/pandas/issues/35762
        # pd.Series([NoneT, 0, 1, 2, 3, 4], name="datetime_sparse", dtype=pd.SparseDtype(np.datetime64)),
        # Pandas dtypes
        pd.Series(
            [0, 1, 2, 3, None],
            name="pd_int64_sparse",
            dtype=pd.SparseDtype(pd.Int64Dtype()),
        ),
        # Pending https://github.com/pandas-dev/pandas/issues/35793
        # pd.Series(
        #     ["a", "b", "c", None],
        #     name="pd_categorical_sparse",
        #     dtype=pd.SparseDtype(pd.CategoricalDtype(['a', 'b', 'c', 'd']))
        # )
    ]

    if int(pd.__version__.split(".")[0]) >= 1:
        pandas_1_series = [
            pd.Series(
                ["Patty", "Valentine", "Upper", "", "", ""],
                name="pd_string_sparse",
                dtype=pd.SparseDtype(pd.StringDtype(), ""),
            ),
            pd.Series(
                [True, False, False, None],
                name="pd_bool_sparse",
                dtype=pd.SparseDtype(pd.BooleanDtype(), None),
            ),
        ]
        test_series.extend(pandas_1_series)

    return test_series

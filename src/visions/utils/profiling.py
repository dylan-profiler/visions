import timeit
import pandas as pd
import numpy as np
import big_o


def big_o_tester(type):
    def inner(test_series):
        try:
            res = big_o.big_o(
                lambda x: x in type,
                lambda n: test_series[0:n],
                max_n=test_series.shape[0],
            )
            return res[0]
        except np.linalg.LinAlgError:
            return np.nan

    return inner


def profile_type(dtype, profile_data, run_count=10, normed_length=100000):
    profile_data = {
        name: pd.Series(np.random.choice(data, normed_length))
        for name, data in profile_data.items()
        if len(data) > 0
    }
    big_O_test = big_o_tester(dtype)
    return [
        {
            "type": dtype,
            "series": name,
            "run count": run_count,
            "average run time": timeit.timeit(lambda: data in dtype, number=run_count)
            / run_count,
            "big O": big_O_test(data),
        }
        for name, data in profile_data.items()
    ]

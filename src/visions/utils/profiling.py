import functools
import timeit

import numpy as np
import pandas as pd


def big_o_tester(test_func):
    import big_o

    @functools.wraps(test_func)
    def inner(test_series):
        try:
            best, _ = big_o.big_o(
                test_func, lambda n: test_series[0:n], max_n=test_series.shape[0]
            )
            return best
        except np.linalg.LinAlgError:
            return np.nan

    return inner


def profile_type(dtype, profile_data, run_count=10, normed_length=100000):
    profile_data = {
        name: pd.Series(np.random.choice(data, normed_length))
        for name, data in profile_data.items()
        if len(data) > 0
    }
    big_O_test = big_o_tester(lambda x: x in dtype)
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


def profile_relation_is_relation(
    relation, profile_data, run_count=10, normed_length=100000
):
    profile_data = {
        name: pd.Series(np.random.choice(data, normed_length))
        for name, data in profile_data.items()
        if len(data) > 0
    }
    big_O_test = big_o_tester(relation.is_relation)
    return [
        {
            "relation": relation,
            "series": name,
            "run count": run_count,
            "average run time": timeit.timeit(
                lambda: relation.is_relation, number=run_count
            )
            / run_count,
            "big O": big_O_test(data),
        }
        for name, data in profile_data.items()
    ]


def profile_relation_transform(
    relation, profile_data, run_count=10, normed_length=100000
):
    profile_data = {
        name: pd.Series(np.random.choice(data, normed_length))
        for name, data in profile_data.items()
        if len(data) > 0
    }
    big_O_test = big_o_tester(relation.transform)
    return [
        {
            "relation": relation,
            "series": name,
            "run count": run_count,
            "average run time": timeit.timeit(
                lambda: relation.transform, number=run_count
            )
            / run_count,
            "big O": big_O_test(data),
        }
        for name, data in profile_data.items()
    ]

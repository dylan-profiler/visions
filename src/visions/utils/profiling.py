import timeit
import pandas as pd
import numpy as np


def profile_type(dtype, profile_data, run_count=10, normed_length=100000):
    profile_data = {
        name: pd.Series(np.random.choice(data, normed_length))
        for name, data in profile_data.items()
        if len(data) > 0
    }
    return [
        {
            "type": dtype,
            "series": name,
            "run count": run_count,
            "average run time": timeit.timeit(lambda: data in dtype, number=run_count)
            / run_count,
        }
        for name, data in profile_data.items()
    ]

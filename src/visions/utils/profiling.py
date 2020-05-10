import timeit


def profile_type(dtype, profile_data, run_count=1000):
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

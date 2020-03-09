import pandas as pd


def base_summary(series: pd.Series) -> dict:
    """Summary for every series

    Args:
        series: series to summarize

    Returns:
        A summary of the series including `frequencies`, `n_records`, `memory_size`, `dtype` and `types`.
    """
    summary = {
        "frequencies": series.value_counts().to_dict(),
        "n_records": series.shape[0],
        "memory_size": series.memory_usage(deep=True),
        "dtype": series.dtype,
        "types": series.map(lambda x: type(x).__name__).value_counts().to_dict(),
    }

    return summary

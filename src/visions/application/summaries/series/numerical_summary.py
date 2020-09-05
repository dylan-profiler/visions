from typing import Any, Tuple, Union

import numpy as np
import pandas as pd


def named_aggregate_summary(series: pd.Series, key: str):
    summary = {
        f"max_{key}": np.max(series),
        f"mean_{key}": np.mean(series),
        f"median_{key}": np.median(series),
        f"min_{key}": np.min(series),
    }

    return summary


def mad(arr, m=None):
    """Median Absolute Deviation: a "Robust" version of standard deviation.
    Indices variability of the sample.
    https://en.wikipedia.org/wiki/Median_absolute_deviation
    """
    if m is None:
        m = np.median(arr)
    return np.median(np.abs(arr - m))


def numerical_summary(
    series: pd.Series,
    quantiles=(0.05, 0.25, 0.5, 0.75, 0.95),
    count=None,
    is_unique=None,
    return_values=False,
) -> Union[dict, Tuple[dict, Any]]:
    """

    Args:
        series: series to summarize

    Returns:

    """

    if count is None:
        count = series.count()

    values = series.values
    present_values = values[~np.isnan(values)]
    finite_mask = np.isfinite(present_values)
    finite_values = present_values[finite_mask]

    summary = {
        "mean": np.mean(present_values),
        "std": np.std(present_values, ddof=1),
        "min": np.min(present_values),
        "max": np.max(present_values),
        # Unbiased kurtosis obtained using Fisher's definition (kurtosis of normal == 0.0). Normalized by N-1.
        "kurt": series.kurt(),
        # Unbiased skew normalized by N-1
        "skew": series.skew(),
        "sum": np.sum(present_values),
        "n_infinite": (~finite_mask).sum(),
        "n_zeros": (count - np.count_nonzero(present_values)),
    }

    for percentile, value in series.quantile(quantiles).to_dict().items():
        summary["quantile_{:d}".format(int(percentile * 100))] = value
    summary["median"] = summary["quantile_50"]
    summary["iqr"] = summary["quantile_75"] - summary["quantile_25"]

    summary["mad"] = mad(present_values, summary["quantile_50"])
    summary["variance"] = summary["std"] ** 2
    summary["cv"] = summary["std"] / summary["mean"] if summary["mean"] else np.NaN
    summary["range"] = summary["max"] - summary["min"]

    summary["monotonic_increase"] = series.is_monotonic_increasing
    summary["monotonic_decrease"] = series.is_monotonic_decreasing

    summary["monotonic_increase_strict"] = (
        summary["monotonic_increase"] and series.is_unique
    )
    summary["monotonic_decrease_strict"] = (
        summary["monotonic_decrease"] and series.is_unique
    )

    if return_values:
        return summary, finite_values

    return summary

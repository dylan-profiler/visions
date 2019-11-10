import numpy as np
import pandas as pd


def numerical_summary(series: pd.Series) -> dict:
    """

    Args:
        series: series to summarize

    Returns:

    """
    aggregates = [
        "mean",
        "std",
        "var",
        "max",
        "min",
        "median",
        "kurt",
        "skew",
        "sum",
        "mad",
    ]
    summary = series.agg(aggregates).to_dict()

    quantiles = [0.05, 0.25, 0.5, 0.75, 0.95]
    for percentile, value in series.quantile(quantiles).to_dict().items():
        summary["quantile_{:d}".format(int(percentile * 100))] = value
    summary["iqr"] = summary["quantile_75"] - summary["quantile_25"]

    summary["range"] = summary["max"] - summary["min"]
    summary["cv"] = summary["std"] / summary["mean"] if summary["mean"] else np.NaN

    # TODO: only calculations for histogram, not the plotting
    # summary['image'] = plotting.histogram(series)
    return summary

import numpy as np


def infinite_summary(series):
    summary = {}
    mask = (~np.isfinite(series)) & series.notnull()
    summary["inf_count"] = mask.values.sum()
    summary["perc_inf"] = (
        summary["inf_count"] / series.shape[0] if series.shape[0] > 0 else 0
    )
    return summary

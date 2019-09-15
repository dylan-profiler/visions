import numpy as np


def unique_summary(series):
    summary = {}

    # try:
    n_unique = len(set(series.values))
    # n_unique = series.nunique()
    summary.update(
        {
            "n_unique": n_unique,
            "perc_unique": float(n_unique) / len(series) if len(series) > 0 else np.nan,
        }
    )
    # except Exception:
    #     pass
    return summary


def unique_warnings(summary):
    messages = []
    if summary["n_unique"] == 1:
        messages.append("n_unique:const")
    if summary["p_unique"] == 1.0:
        messages.append("n_unique:unique")
    return messages

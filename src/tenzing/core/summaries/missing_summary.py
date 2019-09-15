import numpy as np


def missing_summary(series):
    mask = series.isna()
    summary = {"na_count": mask.values.sum()}
    summary["perc_na"] = (
        summary["na_count"] / series.shape[0] if series.shape[0] > 0 else np.nan
    )
    return summary

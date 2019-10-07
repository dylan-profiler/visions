import numpy as np
import pandas as pd


def missing_summary(series: pd.Series) -> dict:
    """

    Args:
        series:

    Returns:

    """
    mask = series.isna()
    summary = {"na_count": mask.values.sum()}
    return summary

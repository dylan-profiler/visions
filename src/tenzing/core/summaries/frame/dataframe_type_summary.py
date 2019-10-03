import pandas as pd


def dataframe_type_summary(series_types: dict) -> dict:
    return pd.Series(series_types.values()).value_counts()

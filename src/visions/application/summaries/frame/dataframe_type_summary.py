import pandas as pd


def dataframe_type_summary(series_types: dict) -> dict:
    return {"type_counts": pd.Series(list(series_types.values())).value_counts()}

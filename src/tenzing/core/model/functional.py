from tenzing.core.model.typeset import tenzingTypeset
import pandas as pd


def type_cast(df: pd.DataFrame, typeset: tenzingTypeset) -> tenzingTypeset:
    cast_df = typeset.cast_to_inferred_types(df)
    cast_types = {column: typeset.get_series_type(df[column]) for column in df.columns}
    return cast_df, cast_types


def type_inference(df: pd.DataFrame, typeset: tenzingTypeset) -> tenzingTypeset:
    inferred_types = {column: typeset.infer_series_type(df[column]) for column in df.columns}
    return inferred_types

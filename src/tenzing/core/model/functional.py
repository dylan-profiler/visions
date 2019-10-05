from typing import Tuple

import pandas as pd

from tenzing.core.model.typeset import tenzingTypeset


def type_cast(df: pd.DataFrame, typeset: tenzingTypeset) -> Tuple[pd.DataFrame, dict]:
    """Cast the DataFrame to the inferred types. This has side-effects to the DataFrame. If you want to prevent this,
    simply pass a copy of the original DataFrame.

    Args:
        df: the DataFrame to cast
        typeset: the Typeset in which we cast

    Returns:
        A tuple of the casted DataFrame and the types to which the columns were cast
    """
    cast_df = typeset.cast_to_inferred_types(df)
    cast_types = {column: typeset.get_series_type(df[column]) for column in df.columns}
    return cast_df, cast_types


def type_inference(df: pd.DataFrame, typeset: tenzingTypeset) -> dict:
    """Infer the current types of each column in the DataFrame given the typeset.

    Args:
        df: the DataFrame to infer types on
        typeset: the Typeset that provides the type context

    Returns:
        A dictionary with a mapping from column name to type
    """
    inferred_types = {
        column: typeset.infer_series_type(df[column]) for column in df.columns
    }
    return inferred_types

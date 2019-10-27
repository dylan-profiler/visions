from typing import Tuple
import pandas as pd

from visions.core.model.typeset import VisionsTypeset


def type_cast(df: pd.DataFrame, typeset: VisionsTypeset) -> Tuple[pd.DataFrame, dict]:
    """Casts a dataframe into a typeset by first performing column wise type inference against
    a provided typeset

    Args:
        df: the DataFrame to cast
        typeset: the Typeset in which we cast

    Returns:
        A tuple of the casted DataFrame and the types to which the columns were cast
    """
    cast_df = typeset.cast_to_inferred_types(df)
    cast_types = {
        column: typeset.get_series_type(cast_df[column]) for column in cast_df.columns
    }
    return cast_df, cast_types


def type_inference(df: pd.DataFrame, typeset: VisionsTypeset) -> dict:
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

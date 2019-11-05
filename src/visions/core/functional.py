from typing import Tuple
import pandas as pd

from visions.core.model.typeset import VisionsTypeset, infer_type_path


def cast_and_infer(
    df: pd.DataFrame, typeset: VisionsTypeset
) -> Tuple[pd.DataFrame, dict]:
    """Casts a dataframe into a typeset by first performing column wise type inference against
    a provided typeset

    Args:
        df: the DataFrame to cast
        typeset: the Typeset in which we cast

    Returns:
        A tuple of the casted DataFrame and the types to which the columns were cast
    """
    inferred_values = {
        column: infer_type_path(df[column], typeset.relation_graph)
        for column in df.columns
    }

    inferred_types = {col: inf_type for col, (inf_type, _) in inferred_values.items()}
    inferred_series = {
        col: inf_series for col, (_, inf_series) in inferred_values.items()
    }
    return pd.DataFrame(inferred_series), inferred_types


def type_cast(df: pd.DataFrame, typeset: VisionsTypeset) -> pd.DataFrame:
    """Casts a dataframe into a typeset by first performing column wise type inference against
    a provided typeset

    Args:
        df: the DataFrame to cast
        typeset: the Typeset in which we cast

    Returns:
        A tuple of the casted DataFrame and the types to which the columns were cast
    """
    df, _ = cast_and_infer(df, typeset)
    return df


def type_inference(df: pd.DataFrame, typeset: VisionsTypeset) -> dict:
    """Infer the current types of each column in the DataFrame given the typeset.

    Args:
        df: the DataFrame to infer types on
        typeset: the Typeset that provides the type context

    Returns:
        A dictionary with a mapping from column name to type
    """
    inferred_types = {
        column: infer_type_path(df[column], typeset.relation_graph)[0]
        for column in df.columns
    }
    return inferred_types

import pandas as pd

from visions.core.model.typeset import VisionsTypeset


def type_cast(df: pd.DataFrame, typeset: VisionsTypeset) -> pd.DataFrame:
    """Casts a dataframe into a typeset by first performing column wise type inference against
    a provided typeset

    Args:
        df: the DataFrame to cast
        typeset: the Typeset in which we cast

    Returns:
        A tuple of the casted DataFrame and the types to which the columns were cast
    """
    return typeset.cast_frame(df)


def type_inference(df: pd.DataFrame, typeset: VisionsTypeset) -> dict:
    """Infer the current types of each column in the DataFrame given the typeset.

    Args:
        df: the DataFrame to infer types on
        typeset: the Typeset that provides the type context

    Returns:
        A dictionary with a mapping from column name to type
    """

    return typeset.infer_frame_type(df)


def type_detect(df: pd.DataFrame, typeset: VisionsTypeset) -> dict:
    """Detect the type in the base graph

    Args:
        df: the DataFrame to detect types on
        typeset: the Typeset that provides the type context

    Returns:
        A dictionary with a mapping from column name to type
    """
    return typeset.detect_frame_type(df)

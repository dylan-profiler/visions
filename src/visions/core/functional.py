from typing import Dict, Type

import pandas as pd

from visions.core.model.type import VisionsBaseType
from visions.core.model.typeset import VisionsTypeset


def type_cast_frame(df: pd.DataFrame, typeset: VisionsTypeset) -> pd.DataFrame:
    """Casts a DataFrame into a typeset by first performing column wise type inference against
    a provided typeset

    Args:
        df: the DataFrame to cast
        typeset: the Typeset in which we cast

    Returns:
        A tuple of the casted DataFrame and the types to which the columns were cast
    """
    return typeset.cast_frame(df)


def type_cast_series(series: pd.Series, typeset: VisionsTypeset) -> pd.Series:
    """

    Args:
        series:
        typeset:

    Returns:

    """
    return typeset.cast_series(series)


def type_cast_and_infer_frame(
    df: pd.DataFrame, typeset: VisionsTypeset
) -> pd.DataFrame:
    """Casts a DataFrame into a typeset by first performing column wise type inference against
    a provided typeset

    Args:
        df: the DataFrame to cast
        typeset: the Typeset in which we cast

    Returns:
        A tuple of the casted DataFrame and the types to which the columns were cast
    """
    return typeset.cast_and_infer_frame(df)


def type_cast_and_infer_series(series: pd.Series, typeset: VisionsTypeset) -> pd.Series:
    """

    Args:
        series:
        typeset:

    Returns:

    """
    return typeset.cast_and_infer_series(series)


def type_inference_frame(
    df: pd.DataFrame, typeset: VisionsTypeset
) -> Dict[str, Type[VisionsBaseType]]:
    """Infer the current types of each column in the DataFrame given the typeset.

    Args:
        df: the DataFrame to infer types on
        typeset: the Typeset that provides the type context

    Returns:
        A dictionary with a mapping from column name to type
    """

    return typeset.infer_frame_type(df)


def type_inference_series(
    series: pd.Series, typeset: VisionsTypeset
) -> Type[VisionsBaseType]:
    """

    Args:
        series:
        typeset:

    Returns:

    """
    return typeset.infer_series_type(series)


def type_detect_frame(
    df: pd.DataFrame, typeset: VisionsTypeset
) -> Dict[str, Type[VisionsBaseType]]:
    """Detect the type in the base graph

    Args:
        df: the DataFrame to detect types on
        typeset: the Typeset that provides the type context

    Returns:
        A dictionary with a mapping from column name to type
    """
    return typeset.detect_frame_type(df)


def type_detect_series(
    series: pd.Series, typeset: VisionsTypeset
) -> Type[VisionsBaseType]:
    """

    Args:
        series:
        typeset:

    Returns:

    """
    return typeset.detect_series_type(series)

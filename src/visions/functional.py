from typing import Dict, Type, List, Tuple

import pandas as pd

from visions.types.type import VisionsBaseType
from visions.typesets.typeset import VisionsTypeset


def cast_frame(df: pd.DataFrame, typeset: VisionsTypeset) -> pd.DataFrame:
    """Casts a DataFrame into a typeset by first performing column wise type inference against
    a provided typeset

    Args:
        df: the DataFrame to cast
        typeset: the Typeset in which we cast

    Returns:
        A tuple of the casted DataFrame and the types to which the columns were cast
    """
    return typeset.cast_frame(df)


def cast_series(series: pd.Series, typeset: VisionsTypeset) -> pd.Series:
    """Casts the series

    Args:
        series: the Series to infer the type of
        typeset: the Typeset that provides the type context

    Returns:
        The converted series
    """
    return typeset.cast_series(series)


def cast_and_infer_frame(
    df: pd.DataFrame, typeset: VisionsTypeset
) -> Tuple[pd.DataFrame, dict]:
    """Casts a DataFrame into a typeset by first performing column wise type inference against
    a provided typeset

    Args:
        df: the DataFrame to cast
        typeset: the Typeset in which we cast

    Returns:
        A tuple of the casted DataFrame and the types to which the columns were cast
    """
    return typeset.cast_and_infer_frame(df)


def cast_and_infer_series(
    series: pd.Series, typeset: VisionsTypeset
) -> Tuple[Type[VisionsBaseType], pd.Series]:
    """Cast the series and perform type inference

    Args:
        series: the Series to infer the type of
        typeset: the Typeset that provides the type context

    Returns:
        The inferred type and the converted series
    """
    return typeset.cast_and_infer_series(series)


def infer_frame_type(
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


def infer_series_type(
    series: pd.Series, typeset: VisionsTypeset
) -> Type[VisionsBaseType]:
    """Infer the current type of the series given the typeset

    Args:
        series: the Series to infer the type of
        typeset: the Typeset that provides the type context

    Returns:
        The inferred type of the series
    """
    return typeset.infer_series_type(series)


def detect_frame_type(
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


def detect_series_type(
    series: pd.Series, typeset: VisionsTypeset
) -> Type[VisionsBaseType]:
    """Detect the type in the base graph

    Args:
        series: the Series to detect the type of
        typeset: the Typeset that provides the type context

    Returns:
        The detected type
    """
    return typeset.detect_series_type(series)


def compare_detect_inference_frame(
    df: pd.DataFrame, typeset: VisionsTypeset
) -> List[Tuple[str, Type[VisionsBaseType], Type[VisionsBaseType]]]:
    """Compare the types given by inference on the base graph and the relational graph

    Args:
        df: the DataFrame to detect types on
        typeset: the Typeset that provides the type context

    Examples:
        >>> for column, type_before, type_after in compare_detect_inference_frame(df, typeset):
        >>>    print(f"{column} was {type_before} is {type_after}")

    See Also:
        :doc:`type_inference_report_frame <visions.functional.type_inference_report_frame>`: Formatted report of the output of this function
    """
    comparisons = []
    detected_types = detect_frame_type(df, typeset)
    inferred_types = infer_frame_type(df, typeset)
    for key in detected_types.keys() & inferred_types.keys():
        comparisons.append((key, detected_types[key], inferred_types[key]))
    return comparisons


def type_inference_report_frame(df, typeset) -> str:
    """Return formatted report of the output of `compare_detect_inference_frame`.

    Args:
        df: the DataFrame to detect types on
        typeset: the Typeset that provides the type context

    Returns:
        Text-based comparative type inference report

    Examples:
        >>> import pandas as pd
        >>> from visions.functional import type_inference_report_frame
        >>> from visions.typesets import StandardSet
        >>>
        >>> typeset = StandardSet()
        >>> df = pd.read_csv('dataset.csv')
        >>>
        >>> report = type_inference_report_frame(df, typeset)
        >>> print(report)
    """
    padding = 5
    max_column_length = max([len(column) for column in df.columns]) + padding
    max_type_length = 30

    report = ""
    change_count = 0
    for column, type_before, type_after in compare_detect_inference_frame(df, typeset):
        changed = type_before != type_after
        if changed:
            fill = "!="
            change_count += 1
        else:
            fill = "=="
        report += "{column: <{max_column_length}} {type_before: <{max_type_length}} {fill} {type_after: <{max_type_length}} \n".format(
            column=column,
            max_column_length=max_column_length,
            type_before=str(type_before),
            type_after=str(type_after),
            max_type_length=max_type_length,
            fill=fill,
        )
    report += "In total {change_count} out of {type_count} types were changed.\n".format(
        change_count=change_count, type_count=len(df.columns)
    )
    return report

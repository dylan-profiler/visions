from typing import Dict, List, Tuple, Type, Union, Any, cast

from functools import singledispatch
import pandas as pd

from visions.types.type import VisionsBaseType
from visions.typesets.typeset import VisionsTypeset


def cast_to_detected(
    data: Union[pd.Series, pd.DataFrame], typeset: VisionsTypeset
) -> Union[pd.Series, pd.DataFrame]:
    """Casts a DataFrame into a typeset by first performing column wise type inference against
    a provided typeset

    Args:
        data: the DataFrame to cast
        typeset: the Typeset in which we cast

    Returns:
        A tuple of the casted DataFrame and the types to which the columns were cast
    """
    return typeset.cast_to_detected(data)


def cast_to_inferred(
    data: Union[pd.Series, pd.DataFrame], typeset: VisionsTypeset
) -> Union[pd.Series, pd.DataFrame]:
    """Casts a DataFrame into a typeset by first performing column wise type inference against
    a provided typeset

    Args:
        data: the DataFrame to cast
        typeset: the Typeset in which we cast

    Returns:
        A tuple of the casted DataFrame and the types to which the columns were cast
    """
    return typeset.cast_to_inferred(data)


@singledispatch
def infer_type(data: Any, typeset: VisionsTypeset) -> Union[Dict[str, Type[VisionsBaseType]], Type[VisionsBaseType]]:
    """Infer the type in the base graph

    Args:
        data: the data to detect types on
        typeset: the Typeset that provides the type context

    Returns:
        A dictionary with a mapping from column name to type
    """
    return typeset.infer_type(data)


@infer_type.register(pd.Series)
def infer_type_series(series: pd.Series, typeset: VisionsTypeset) -> Type[VisionsBaseType]:
    result = typeset.infer_type(series)
    return cast(Type[VisionsBaseType], result)


@infer_type.register(pd.DataFrame)
def infer_type_df(df: pd.DataFrame, typeset: VisionsTypeset) -> Dict[str, Type[VisionsBaseType]]:
    result = typeset.infer_type(df)
    return cast(Dict[str, Type[VisionsBaseType]], result)


@singledispatch
def detect_type(data: Any, typeset: VisionsTypeset) -> Union[Dict[str, Type[VisionsBaseType]], Type[VisionsBaseType]]:
    """Detect the type in the base graph

    Args:
        data: the data to detect types on
        typeset: the Typeset that provides the type context

    Returns:
        A dictionary with a mapping from column name to type
    """
    return typeset.detect_type(data)


@detect_type.register(pd.Series)
def detect_type_series(series: pd.Series, typeset: VisionsTypeset) -> Type[VisionsBaseType]:
    result = typeset.detect_type(series)
    return cast(Type[VisionsBaseType], result)


@detect_type.register(pd.DataFrame)
def detect_type_dataframe(df: pd.DataFrame, typeset: VisionsTypeset) -> Dict[str, Type[VisionsBaseType]]:
    result = typeset.detect_type(df)
    return cast(Dict[str, Type[VisionsBaseType]], result)


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
    detected_types = detect_type(df, typeset)
    inferred_types = infer_type(df, typeset)

    assert isinstance(detected_types, dict) and isinstance(inferred_types, dict)  # Placate the MyPy Gods

    for key in detected_types.keys() & inferred_types.keys():
        comparisons.append(
            (key, detected_types[key], inferred_types[key])
        )
    return comparisons


def type_inference_report_frame(df: pd.DataFrame, typeset: VisionsTypeset) -> str:
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
    report += (
        "In total {change_count} out of {type_count} types were changed.\n".format(
            change_count=change_count, type_count=len(df.columns)
        )
    )
    return report

from typing import Dict, List, Sequence, Tuple, Type, Union

import pandas as pd

from visions.types.type import VisionsBaseType
from visions.typesets.typeset import VisionsTypeset

T = Type[VisionsBaseType]


def cast_to_detected(data: Sequence, typeset: VisionsTypeset) -> Sequence:
    """Casts a DataFrame into a typeset by first performing column wise type detection against
    a provided typeset

    Args:
        data: the DataFrame to cast
        typeset: the Typeset in which we cast

    Returns:
        A tuple of the casted DataFrame and the types to which the columns were cast
    """
    return typeset.cast_to_detected(data)


def cast_to_inferred(data: Sequence, typeset: VisionsTypeset) -> Sequence:
    """Casts a DataFrame into a typeset by first performing column wise type inference against
    a provided typeset

    Args:
        data: the DataFrame to cast
        typeset: the Typeset in which we cast

    Returns:
        A tuple of the casted DataFrame and the types to which the columns were cast
    """
    return typeset.cast_to_inferred(data)


def infer_type(data: Sequence, typeset: VisionsTypeset) -> Union[Dict[str, T], T]:
    """Infer the current types of each column in the DataFrame given the typeset.

    Args:
        data: the DataFrame to infer types on
        typeset: the Typeset that provides the type context

    Returns:
        A dictionary with a mapping from column name to type
    """
    return typeset.infer_type(data)


def detect_type(data: Sequence, typeset: VisionsTypeset) -> Union[Dict[str, T], T]:
    """Detect the type in the base graph

    Args:
        data: the DataFrame to detect types on
        typeset: the Typeset that provides the type context

    Returns:
        A dictionary with a mapping from column name to type
    """
    return typeset.detect_type(data)


def compare_detect_inference_frame(
    data: Sequence, typeset: VisionsTypeset
) -> List[Tuple[str, T, T]]:
    """Compare the types given by inference on the base graph and the relational graph

    Args:
        data: the sequence to detect types on
        typeset: the Typeset that provides the type context

    Examples:
        >>> for column, type_before, type_after in compare_detect_inference_frame(data, typeset):
        >>>    print(f"{column} was {type_before} is {type_after}")

    See Also:
        :doc:`type_inference_report_frame <visions.functional.type_inference_report_frame>`:
            Formatted report of the output of this function
    """
    comparisons = []
    detected_types = detect_type(data, typeset)
    inferred_types = infer_type(data, typeset)

    assert isinstance(detected_types, dict) and isinstance(
        inferred_types, dict
    )  # Placate the MyPy Gods

    for key in detected_types.keys() & inferred_types.keys():
        comparisons.append((key, detected_types[key], inferred_types[key]))
    return comparisons


# TODO: make independent of pandas
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
        report += (
            f"{column: <{max_column_length}} {type_before: <{max_type_length}} "
            f"{fill} "
            f"{type_after: <{max_type_length}} \n"
        )
    report += (
        "In total {change_count} out of {type_count} types were changed.\n".format(
            change_count=change_count, type_count=len(df.columns)
        )
    )
    return report

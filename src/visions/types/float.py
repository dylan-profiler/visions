from typing import Sequence

import numpy as np
import pandas as pd
import pandas.api.types as pdt

from visions.relations import IdentityRelation, InferenceRelation, TypeRelation
from visions.types.type import VisionsBaseType
from visions.utils.coercion import test_utils
from visions.utils.warning_handling import suppress_warnings
from visions.utils.series_utils import func_nullable_series_contains


def test_string_leading_zeros(series: pd.Series, coerced_series: pd.Series):
    if coerced_series.hasnans:
        notna = coerced_series.notna()
        coerced_series = coerced_series[notna]

        if coerced_series.empty:
            return False
        series = series[notna]

    return not any(s[0] == "0" for s in series[coerced_series > 1])


def test_string_is_float(series: pd.Series) -> bool:
    coerced_series = test_utils.option_coercion_evaluator(string_to_float)(series)
    if coerced_series is not None and coerced_series in Float:
        return test_string_leading_zeros(series, coerced_series)

    return False


def string_to_float(series: pd.Series) -> pd.Series:
    # Slightly faster to check for the character if it's not present than to
    # attempt the replacement
    # if any("," in x for x in series.dropna()):
    #     series = series.str.replace(",", "")

    return to_float(series)


def test_is_float(series: pd.Series) -> bool:
    coerced_series = test_utils.option_coercion_evaluator(to_float)(series)
    return coerced_series is not None and coerced_series in Float


def to_float(series: pd.Series) -> pd.Series:
    return series.astype(float)


def _get_relations(cls) -> Sequence[TypeRelation]:
    from visions.types import Generic, String, Complex

    relations = [
        IdentityRelation(cls, Generic),
        InferenceRelation(
            cls, String, relationship=test_string_is_float, transformer=string_to_float
        ),
        InferenceRelation(
            cls,
            Complex,
            relationship=lambda s: all(np.imag(s.values) == 0),
            transformer=suppress_warnings(to_float),
        ),
    ]
    return relations


class Float(VisionsBaseType):
    """**Float** implementation of :class:`visions.types.type.VisionsBaseType`.

    Examples:
        >>> x = pd.Series([1.0, 2.5, 5.0, np.nan])
        >>> x in visions.Float
        True
    """

    @classmethod
    def get_relations(cls) -> Sequence[TypeRelation]:
        return _get_relations(cls)

    @classmethod
    def contains_op(cls, series: pd.Series) -> bool:
        return pdt.is_float_dtype(series)

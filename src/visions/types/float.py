from typing import Sequence

import numpy as np
import pandas as pd
from pandas.api import types as pdt

from visions.relations import IdentityRelation, InferenceRelation, TypeRelation
from visions.types.type import VisionsBaseType
from visions.utils.coercion import test_utils
from visions.utils.series_utils import (
    nullable_series_contains,
    series_not_empty,
    series_not_sparse,
)
from visions.utils.warning_handling import suppress_warnings


def test_string_leading_zeros(series: pd.Series, coerced_series: pd.Series):
    if coerced_series.hasnans:
        notna = coerced_series.notna()
        coerced_series = coerced_series[notna]

        if coerced_series.empty:
            return False
        series = series[notna]
    return not any(s[0] == "0" for s in series[coerced_series > 1])


# @func_nullable_series_contains
def string_to_float(series: pd.Series, state: dict) -> pd.Series:
    # Slightly faster to check for the character if it's not present than to
    # attempt the replacement
    # if any("," in x for x in series):
    #     series = series.str.replace(",", "")
    return series.astype(float)


def f(s):
    return s.astype(float)


def string_is_float(series: pd.Series, state: dict) -> bool:
    coerced_series = test_utils.option_coercion_evaluator(f)(series)

    return (
        coerced_series is not None
        and coerced_series in Float
        and test_string_leading_zeros(series, coerced_series)
    )


def to_float(series: pd.Series, state: dict) -> pd.Series:
    return series.astype(float)


def complex_is_float(series, state: dict):
    return all(np.imag(series.values) == 0)


def complex_to_float(series, state: dict):
    return suppress_warnings(to_float)(series, state)


def _get_relations(cls) -> Sequence[TypeRelation]:
    from visions.types import Complex, Generic, String

    relations = [
        IdentityRelation(cls, Generic),
        InferenceRelation(
            cls, String, relationship=string_is_float, transformer=string_to_float
        ),
        InferenceRelation(
            cls,
            Complex,
            relationship=complex_is_float,
            transformer=complex_to_float,
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
    @series_not_sparse
    @nullable_series_contains
    @series_not_empty
    def contains_op(cls, series: pd.Series, state: dict) -> bool:
        return pdt.is_float_dtype(series)

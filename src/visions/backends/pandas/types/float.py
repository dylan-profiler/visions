import numpy as np
import pandas as pd
from pandas.api import types as pdt

from visions.backends.pandas import test_utils
from visions.backends.pandas.series_utils import series_not_empty, series_not_sparse
from visions.types.float import (
    complex_is_float,
    complex_to_float,
    float_contains,
    string_is_float,
    string_to_float,
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


@string_to_float.register(pd.Series)
def _(series: pd.Series, state: dict) -> pd.Series:
    # Slightly faster to check for the character if it's not present than to
    # attempt the replacement
    # if any("," in x for x in series):
    #     series = series.str.replace(",", "")
    return series.astype(float)


@string_is_float.register(pd.Series)
def _(series: pd.Series, state: dict) -> bool:
    coerced_series = test_utils.option_coercion_evaluator(lambda s: s.astype(float))(
        series
    )

    return (
        coerced_series is not None
        and float_contains(coerced_series, state)
        and test_string_leading_zeros(series, coerced_series)
    )


@complex_is_float.register(pd.Series)
def _(series: pd.Series, state: dict) -> bool:
    return all(np.imag(series.values) == 0)


@complex_to_float.register(pd.Series)
def _(series: pd.Series, state: dict) -> pd.Series:
    return suppress_warnings(lambda s: s.astype(float))(series)


@float_contains.register(pd.Series)
@series_not_empty
@series_not_sparse
def _(series: pd.Series, state: dict) -> bool:
    return pdt.is_float_dtype(series)

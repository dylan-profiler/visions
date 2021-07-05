import numpy as np
import pandas as pd
from pandas.api import types as pdt

from visions.backends.pandas import test_utils
from visions.backends.pandas.series_utils import (
    series_handle_nulls,
    series_not_empty,
    series_not_sparse,
)
from visions.types.complex import Complex
from visions.types.float import Float
from visions.types.string import String
from visions.utils.warning_handling import suppress_warnings


def test_string_leading_zeros(series: pd.Series, coerced_series: pd.Series):
    if coerced_series.hasnans:
        notna = coerced_series.notna()
        coerced_series = coerced_series[notna]

        if coerced_series.empty:
            return False
        series = series[notna]
    return not any(s[0] == "0" for s in series[coerced_series > 1])


@Float.register_relationship(String, pd.Series)
@series_handle_nulls
def string_is_float(series: pd.Series, state: dict) -> bool:
    coerced_series = test_utils.option_coercion_evaluator(lambda s: s.astype(float))(
        series
    )

    return (
        coerced_series is not None
        and float_contains(coerced_series, state)
        and test_string_leading_zeros(series, coerced_series)
    )


@Float.register_transformer(String, pd.Series)
def string_to_float(series: pd.Series, state: dict) -> pd.Series:
    # Slightly faster to check for the character if it's not present than to
    # attempt the replacement
    # if any("," in x for x in series):
    #     series = series.str.replace(",", "")
    return series.astype(float)


@Float.register_relationship(Complex, pd.Series)
def complex_is_float(series: pd.Series, state: dict) -> bool:
    return all(np.imag(series.values) == 0)


@Float.register_transformer(Complex, pd.Series)
def complex_to_float(series: pd.Series, state: dict) -> pd.Series:
    return suppress_warnings(lambda s: s.astype(float))(series)


@Float.contains_op.register
@series_not_sparse
@series_handle_nulls
@series_not_empty
def float_contains(series: pd.Series, state: dict) -> bool:
    return pdt.is_float_dtype(series)

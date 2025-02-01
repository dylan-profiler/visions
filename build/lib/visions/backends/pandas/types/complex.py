import math
from typing import Union

import numpy as np
import pandas as pd
from pandas.api import types as pdt

from visions.backends.pandas import test_utils
from visions.backends.pandas.series_utils import series_not_empty, series_not_sparse
from visions.backends.shared.parallelization_engines import pandas_apply
from visions.types.complex import Complex
from visions.types.string import String


def imaginary_in_string(
    series: pd.Series, imaginary_indicator: tuple = ("j", "i")
) -> bool:
    return any(any(v in s for v in imaginary_indicator) for s in series)


def convert_val_to_complex(val: str) -> Union[complex, float]:
    result = complex(val)
    return (
        np.nan if any(math.isnan(val) for val in (result.real, result.imag)) else result
    )


def convert_to_complex_series(series: pd.Series) -> pd.Series:
    return pandas_apply(series, convert_val_to_complex)


@Complex.register_relationship(String, pd.Series)
def string_is_complex(series: pd.Series, state: dict) -> bool:
    coerced_series = test_utils.option_coercion_evaluator(convert_to_complex_series)(
        series
    )

    return (
        coerced_series is not None
        and not all(v.imag == 0 for v in coerced_series.dropna())
        and imaginary_in_string(series)
    )


@Complex.register_transformer(String, pd.Series)
def string_to_complex(series: pd.Series, state: dict) -> pd.Series:
    return convert_to_complex_series(series)


@Complex.contains_op.register
@series_not_sparse
@series_not_empty
def complex_contains(series: pd.Series, state: dict) -> bool:
    return pdt.is_complex_dtype(series)

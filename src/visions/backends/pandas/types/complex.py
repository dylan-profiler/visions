import pandas as pd
from pandas.api import types as pdt

from visions.backends.pandas import test_utils
from visions.backends.pandas.series_utils import series_not_empty, series_not_sparse
from visions.types.complex import complex_contains, string_is_complex, string_to_complex
from visions.types.float import string_is_float


def test_imaginary_in_string(
    series: pd.Series, imaginary_indicator: tuple = ("j", "i")
):
    return any(any(v in s for v in imaginary_indicator) for s in series)


@string_is_complex.register(pd.Series)
def _(series: pd.Series, state: dict) -> bool:
    def f(s):
        return s.apply(complex)

    coerced_series = test_utils.option_coercion_evaluator(f)(series)
    return (
        coerced_series is not None
        and not string_is_float(series, state)
        and test_imaginary_in_string(series)
    )


@complex_contains.register(pd.Series)
@series_not_sparse
@series_not_empty
def _(series: pd.Series, state: dict) -> bool:
    return pdt.is_complex_dtype(series)


@string_to_complex.register(pd.Series)
def _(series: pd.Series, state: dict) -> bool:
    return series.apply(complex)

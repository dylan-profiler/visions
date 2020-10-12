import pandas as pd
from pandas.api import types as pdt

from visions.backends.pandas_be import test_utils
from visions.backends.pandas_be.series_utils import series_not_empty, series_not_sparse
from visions.backends.pandas_be.types.float import string_is_float
from visions.types.complex import Complex
from visions.types.string import String


def imaginary_in_string(series: pd.Series, imaginary_indicator: tuple = ("j", "i")):
    return any(any(v in s for v in imaginary_indicator) for s in series)


@Complex.register_relationship(String, pd.Series)
def string_is_complex(series: pd.Series, state: dict) -> bool:
    def f(s):
        return s.apply(complex)

    coerced_series = test_utils.option_coercion_evaluator(f)(series)
    return (
        coerced_series is not None
        and not string_is_float(series, state)
        and imaginary_in_string(series)
    )


@Complex.register_transformer(String, pd.Series)
def string_to_complex(series: pd.Series, state: dict) -> bool:
    return series.apply(complex)


@Complex.contains_op.register
@series_not_sparse
@series_not_empty
def complex_contains(series: pd.Series, state: dict) -> bool:
    return pdt.is_complex_dtype(series)

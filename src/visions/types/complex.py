from typing import Sequence

import pandas as pd
from pandas.api import types as pdt

from visions.relations import IdentityRelation, InferenceRelation, TypeRelation
from visions.types.float import string_is_float
from visions.types.type import VisionsBaseType
from visions.utils.coercion import test_utils
from visions.utils.series_utils import series_not_empty, series_not_sparse


def test_imaginary_in_string(
    series: pd.Series, imaginary_indicator: tuple = ("j", "i")
):
    return any(any(v in s for v in imaginary_indicator) for s in series)


def string_is_complex(series, state: dict) -> bool:
    def f(s):
        return s.apply(complex)

    coerced_series = test_utils.option_coercion_evaluator(f)(series)
    return (
        coerced_series is not None
        and not string_is_float(series, state)
        and test_imaginary_in_string(series)
    )


def to_complex(series: pd.Series, state: dict) -> bool:
    return series.apply(complex)


def _get_relations(cls) -> Sequence[TypeRelation]:
    from visions.types import Generic, String

    relations = [
        IdentityRelation(cls, Generic),
        InferenceRelation(
            cls, String, relationship=string_is_complex, transformer=to_complex
        ),
    ]
    return relations


class Complex(VisionsBaseType):
    """**Complex** implementation of :class:`visions.types.type.VisionsBaseType`.

    Examples:
        >>> import numpy as np
        >>> x = pd.Series([np.complex(0, 0), np.complex(1, 2), np.complex(3, -1), np.nan])
        >>> x in visions.Complex
        True
    """

    @classmethod
    def get_relations(cls) -> Sequence[TypeRelation]:
        return _get_relations(cls)

    @classmethod
    @series_not_sparse
    @series_not_empty
    def contains_op(cls, series: pd.Series, state: dict) -> bool:
        return pdt.is_complex_dtype(series)

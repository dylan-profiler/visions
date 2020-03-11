from typing import Sequence

import pandas.api.types as pdt
import numpy as np
import pandas as pd

from visions.relations import IdentityRelation, InferenceRelation, TypeRelation
from visions.types import VisionsBaseType
from visions.utils.coercion import test_utils
from visions.utils.warning_handling import suppress_warnings


def test_string_is_float(series) -> bool:
    coerced_series = test_utils.option_coercion_evaluator(to_float)(series)
    return coerced_series is not None and coerced_series in Float


def to_float(series: pd.Series) -> bool:
    return series.astype(float)


def _get_relations(cls) -> Sequence[TypeRelation]:
    from visions.types import Generic, String, Complex

    relations = [
        IdentityRelation(cls, Generic),
        InferenceRelation(
            cls, String, relationship=test_string_is_float, transformer=to_float
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

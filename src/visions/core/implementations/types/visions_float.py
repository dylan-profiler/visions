import pandas.api.types as pdt
import numpy as np
import pandas as pd

from visions.core.model.relations import IdentityRelation, InferenceRelation
from visions.core.model.type import VisionsBaseType
from visions.utils.coercion import test_utils
from visions.utils.warning_handling import suppress_warnings


def test_string_is_float(series):
    coerced_series = test_utils.option_coercion_evaluator(to_float)(series)
    return coerced_series is not None and coerced_series in visions_float


def to_float(series: pd.Series) -> bool:
    return series.astype(float)


def _get_relations():
    from visions.core.implementations.types import (
        visions_generic,
        visions_string,
        visions_complex,
    )

    relations = [
        IdentityRelation(visions_float, visions_generic),
        InferenceRelation(
            visions_float,
            visions_string,
            relationship=test_string_is_float,
            transformer=to_float,
        ),
        InferenceRelation(
            visions_float,
            visions_complex,
            relationship=lambda s: all(np.imag(s.values) == 0),
            transformer=suppress_warnings(to_float),
        ),
    ]
    return relations


class visions_float(VisionsBaseType):
    """**Float** implementation of :class:`visions.core.model.type.VisionsBaseType`.

    Examples:
        >>> x = pd.Series([1.0, 2.5, 5.0, np.nan])
        >>> x in visions_float
        True
    """

    @classmethod
    def get_relations(cls):
        return _get_relations()

    @classmethod
    def contains_op(cls, series: pd.Series) -> bool:
        return pdt.is_float_dtype(series)

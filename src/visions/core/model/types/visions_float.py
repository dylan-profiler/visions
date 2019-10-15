import pandas.api.types as pdt
import numpy as np
import pandas as pd

from visions.core.model.model_relation import relation_conf
from visions.core.model.models import VisionsBaseType
from visions.core.model.types.visions_integer import visions_integer
from visions.utils.coercion import test_utils
from visions.utils.warning_handling import suppress_warnings


def test_string_is_float(series):
    coerced_series = test_utils.option_coercion_evaluator(to_float)(series)
    return coerced_series is not None and coerced_series in visions_float


def to_float(series: pd.Series) -> bool:
    return series.astype(float)


class visions_float(VisionsBaseType):
    """**Float** implementation of :class:`visions.core.models.VisionsBaseType`.
    >>> x = pd.Series([1.0, 2.5, 5.0, np.nan])
    >>> x in visions_float
    True
    """

    @classmethod
    def get_relations(cls):
        from visions.core.model.types import (
            visions_generic,
            visions_string,
            visions_complex,
        )

        relations = {
            visions_generic: relation_conf(inferential=False),
            visions_string: relation_conf(
                relationship=test_string_is_float,
                transformer=to_float,
                inferential=True,
            ),
            visions_complex: relation_conf(
                relationship=lambda s: all(np.imag(s.values) == 0),
                transformer=suppress_warnings(to_float),
                inferential=True,
            ),
        }

        return relations

    @classmethod
    def contains_op(cls, series: pd.Series) -> bool:
        return pdt.is_float_dtype(series)

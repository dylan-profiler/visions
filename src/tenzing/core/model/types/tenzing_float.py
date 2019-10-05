import pandas.api.types as pdt
import numpy as np
import pandas as pd

from tenzing.core.model.model_relation import relation_conf
from tenzing.core.model.models import tenzing_model
from tenzing.core.model.types.tenzing_integer import tenzing_integer
from tenzing.utils.coercion import test_utils


def test_string_is_float(series):
    coerced_series = test_utils.option_coercion_evaluator(tenzing_float.cast)(
        series
    )
    return coerced_series is not None and coerced_series in tenzing_float


class tenzing_float(tenzing_model):
    """**Float** implementation of :class:`tenzing.core.models.tenzing_model`.
    >>> x = pd.Series([1.0, 2.5, 5.0, np.nan])
    >>> x in tenzing_float
    True
    """

    @classmethod
    def register_relations(cls):
        from tenzing.core.model.types import tenzing_generic, tenzing_string, tenzing_complex

        relations = {
            tenzing_generic: relation_conf(inferential=False),
            tenzing_string: relation_conf(relationship=test_string_is_float, inferential=True),
            tenzing_complex: relation_conf(
                relationship=lambda s: all(np.imag(s.values) == 0),
                transformer=lambda s: s.astype(float),
                inferential=True
            )
        }

        return relations

    @classmethod
    def contains_op(cls, series: pd.Series) -> bool:
        return pdt.is_float_dtype(series) and series not in tenzing_integer

    @classmethod
    def cast_op(cls, series: pd.Series, operation=None) -> bool:
        return series.astype(float)

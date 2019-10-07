import pandas.api.types as pdt
import pandas as pd
import numpy as np

from tenzing.core.model.model_relation import relation_conf
from tenzing.core.model.models import tenzing_model
from tenzing.utils.coercion.test_utils import coercion_map_test, coercion_map


def to_bool(series: pd.Series) -> pd.Series:
    if series.isin({True, False}).all():
        return series.astype(bool)
    elif series.isin({True, False, None, np.nan}).all():
        return series.astype("Bool")
    else:
        raise ValueError(f"Values not supported {series.unique()}")


class tenzing_bool(tenzing_model):
    """**Boolean** implementation of :class:`tenzing.core.models.tenzing_model`.
    >>> x = pd.Series([True, False, False, True])
    >>> x in tenzing_bool
    True

    >>> x = pd.Series([True, False, None])
    >>> x in tenzing_bool
    True
    """

    @classmethod
    def get_relations(cls) -> dict:
        from tenzing.core.model.types import tenzing_generic, tenzing_string, tenzing_integer, tenzing_object

        coercions = [
            {"true": True, "false": False},
            {"y": True, "n": False},
            {"yes": True, "no": False},
        ]

        relations = {
            tenzing_generic: relation_conf(inferential=False),
            # TODO: ensure that series.str.lower() has no side effects
            tenzing_string: relation_conf(
                inferential=True,
                relationship=lambda s: coercion_map_test(coercions)(s.str.lower()),
                transformer=lambda s: to_bool(coercion_map(coercions)(s.str.lower())),
            ),
            tenzing_integer: relation_conf(
                inferential=True,
                relationship=lambda s: s.isin({0, 1, np.nan}).all(),
                transformer=to_bool,
            ),
            tenzing_object: relation_conf(
                inferential=True,
                relationship=lambda s: s.apply(type).apply(lambda v: v in [type(None), bool]).all(),
                transformer=to_bool,
            ),
        }
        return relations

    @classmethod
    def contains_op(cls, series: pd.Series) -> bool:
        return not pdt.is_categorical_dtype(series) and pdt.is_bool_dtype(series)

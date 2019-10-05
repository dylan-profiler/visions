import pandas.api.types as pdt
import pandas as pd

from tenzing.core.model.model_relation import relation_conf
from tenzing.core.model.models import tenzing_model
from tenzing.utils.coercion import test_utils


def to_int(series: pd.Series) -> pd.Series:
    try:
        return series.astype(int)
    except ValueError:
        return series.astype("Int64")


def float_is_int(series: pd.Series) -> bool:
    return series.apply(lambda v: v.is_integer()).any() and series.apply(lambda v: v.is_integer() or v != v).all()


class tenzing_integer(tenzing_model):
    """**Integer** implementation of :class:`tenzing.core.models.tenzing_model`.

    Examples:
        >>> x = pd.Series([1, 2, 3])
        >>> x in tenzing_integer
        True
    """

    @classmethod
    def get_relations(cls):
        from tenzing.core.model.types import (
            tenzing_string,
            tenzing_generic,
            tenzing_float,
        )

        relations = {
            tenzing_generic: relation_conf(inferential=False),
            tenzing_float: relation_conf(
                relationship=float_is_int,
                transformer=to_int,
                inferential=True,
            ),
            tenzing_string: relation_conf(
                relationship=test_utils.coercion_test(to_int),
                transformer=to_int,
                inferential=True,
            ),
        }

        return relations

    @classmethod
    def contains_op(cls, series: pd.Series) -> bool:
        return pdt.is_signed_integer_dtype(series)

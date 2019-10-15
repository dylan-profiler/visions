import pandas.api.types as pdt
import pandas as pd
import numpy as np

from visions.core.model.model_relation import relation_conf
from visions.core.model.models import VisionsBaseType
from visions.utils.coercion import test_utils


def to_int(series: pd.Series) -> pd.Series:
    try:
        return series.astype(int)
    except ValueError:
        return series.astype("Int64")


def float_is_int(series: pd.Series) -> bool:
    def check_equality(series):
        if series.empty or not np.isfinite(series).all():
            return False
        return series.eq(series.astype(int)).all()

    return check_equality(series.dropna() if series.hasnans else series)


class visions_integer(VisionsBaseType):
    """**Integer** implementation of :class:`visions.core.models.VisionsBaseType`.

    Examples:
        >>> x = pd.Series([1, 2, 3])
        >>> x in visions_integer
        True
    """

    @classmethod
    def get_relations(cls):
        from visions.core.model.types import (
            visions_string,
            visions_generic,
            visions_float,
        )

        relations = {
            visions_generic: relation_conf(inferential=False),
            visions_float: relation_conf(
                relationship=float_is_int, transformer=to_int, inferential=True
            ),
            visions_string: relation_conf(
                relationship=test_utils.coercion_test(to_int),
                transformer=to_int,
                inferential=True,
            ),
        }

        return relations

    @classmethod
    def contains_op(cls, series: pd.Series) -> bool:
        return pdt.is_signed_integer_dtype(series)

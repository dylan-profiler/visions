import pandas.api.types as pdt
import pandas as pd
from typing import Sequence

from visions.relations import IdentityRelation, InferenceRelation, TypeRelation
from visions.types import VisionsBaseType, visions_string
from visions.utils.coercion import test_utils


def to_datetime(series: pd.Series) -> pd.Series:
    return pd.to_datetime(series)


def _get_relations(cls) -> Sequence[TypeRelation]:
    from visions.types import visions_generic

    relations = [
        IdentityRelation(cls, visions_generic),
        InferenceRelation(
            cls,
            visions_string,
            relationship=test_utils.coercion_test(to_datetime),
            transformer=to_datetime,
        ),
    ]
    return relations


class visions_datetime(VisionsBaseType):
    """**Datetime** implementation of :class:`visions.core.model.type.VisionsBaseType`.

    Examples:
        >>> x = pd.Series([pd.datetime(2017, 3, 5), pd.datetime(2019, 12, 4)])
        >>> x in visions_datetime
        True
    """

    @classmethod
    def get_relations(cls) -> Sequence[TypeRelation]:
        return _get_relations(cls)

    @classmethod
    def contains_op(cls, series: pd.Series) -> bool:
        return pdt.is_datetime64_any_dtype(series)

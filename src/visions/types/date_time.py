from typing import Sequence

import pandas.api.types as pdt
import pandas as pd

from visions.relations import IdentityRelation, InferenceRelation, TypeRelation
from visions.types import VisionsBaseType
from visions.utils.coercion import test_utils


def to_datetime(series: pd.Series) -> pd.Series:
    return pd.to_datetime(series)


def _get_relations(cls) -> Sequence[TypeRelation]:
    from visions.types import Generic, String

    relations = [
        IdentityRelation(cls, Generic),
        InferenceRelation(
            cls,
            String,
            relationship=test_utils.coercion_test(to_datetime),
            transformer=to_datetime,
        ),
    ]
    return relations


class DateTime(VisionsBaseType):
    """**Datetime** implementation of :class:`visions.types.type.VisionsBaseType`.

    Examples:
        >>> x = pd.Series([pd.datetime(2017, 3, 5), pd.datetime(2019, 12, 4)])
        >>> x in visions.DateTime
        True
    """

    @classmethod
    def get_relations(cls) -> Sequence[TypeRelation]:
        return _get_relations(cls)

    @classmethod
    def contains_op(cls, series: pd.Series) -> bool:
        return pdt.is_datetime64_any_dtype(series)

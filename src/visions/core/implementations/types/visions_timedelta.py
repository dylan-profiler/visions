import pandas.api.types as pdt
import pandas as pd

from visions.core.model.relations import IdentityRelation, InferenceRelation
from visions.core.model.type import VisionsBaseType


def _get_relations():
    from visions.core.implementations.types import visions_generic

    relations = [IdentityRelation(visions_timedelta, visions_generic)]
    return relations


class visions_timedelta(VisionsBaseType):
    """**Timedelta** implementation of :class:`visions.core.model.type.VisionsBaseType`.

    Examples:
        >>> x = pd.Series([pd.Timedelta(days=i) for i in range(3)])
        >>> x in visions_timedelta
        True
    """

    @classmethod
    def get_relations(cls):
        return _get_relations()

    @classmethod
    def contains_op(cls, series: pd.Series) -> bool:
        return pdt.is_timedelta64_dtype(series)

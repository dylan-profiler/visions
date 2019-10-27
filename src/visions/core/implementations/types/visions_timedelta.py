import pandas.api.types as pdt
import pandas as pd

from visions.core.model.model_relation import relation_conf
from visions.core.model.type import VisionsBaseType


class visions_timedelta(VisionsBaseType):
    """**Timedelta** implementation of :class:`visions.core.models.VisionsBaseType`.
    >>> x = pd.Series([pd.Timedelta(days=i) for i in range(3)])
    >>> x in visions_timedelta
    True
    """

    @classmethod
    def get_relations(cls):
        from visions.core.implementations.types import visions_generic

        relations = {visions_generic: relation_conf(inferential=False)}
        return relations

    @classmethod
    def contains_op(cls, series: pd.Series) -> bool:
        return pdt.is_timedelta64_dtype(series)

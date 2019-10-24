import pandas.api.types as pdt
import pandas as pd

from visions.core.model.model_relation import relation_conf
from visions.core.model.type import VisionsBaseType


class visions_object(VisionsBaseType):
    """**Object** implementation of :class:`visions.core.models.VisionsBaseType`.
    >>> x = pd.Series(['a', 1, np.nan])
    >>> x in visions_object
    True
    """

    @classmethod
    def get_relations(cls):
        from visions.core.implementations.types import visions_generic

        relations = {visions_generic: relation_conf(inferential=False)}
        return relations

    @classmethod
    def contains_op(cls, series: pd.Series) -> bool:
        return pdt.is_object_dtype(series)

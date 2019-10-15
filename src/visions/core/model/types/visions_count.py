import pandas.api.types as pdt
import pandas as pd

from visions.core.model.model_relation import relation_conf
from visions.core.model.models import VisionsBaseType


class visions_count(VisionsBaseType):
    """**Existing Path** implementation of :class:`visions.core.models.VisionsBaseType`.
    >>> x = pd.Series([1, 4, 10, 20])
    >>> x in visions_count
    True
    """

    @classmethod
    def get_relations(cls):
        from visions.core.model.types import visions_integer, visions_generic

        relations = {
            # TODO: or inferential=False for integer?
            visions_generic: relation_conf(inferential=False)
        }
        return relations

    @classmethod
    def contains_op(cls, series: pd.Series) -> bool:
        return pdt.is_unsigned_integer_dtype(series)

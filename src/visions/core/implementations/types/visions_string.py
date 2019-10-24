import pandas as pd
import pandas.api.types as pdt

from visions.core.model.model_relation import relation_conf
from visions.core.model.type import VisionsBaseType


class visions_string(VisionsBaseType):
    """**String** implementation of :class:`visions.core.models.VisionsBaseType`.
    >>> x = pd.Series(['rubin', 'carter', 'champion'])
    >>> x in visions_string
    True
    """

    @classmethod
    def get_relations(cls):
        from visions.core.implementations.types import visions_object

        relations = {visions_object: relation_conf(inferential=False)}
        return relations

    @classmethod
    def contains_op(cls, series: pd.Series) -> bool:
        # TODO: without the object check this passes string categories... is there a better way?
        if not pdt.is_object_dtype(series):
            return False
        elif series.hasnans:
            series = series.dropna()
            if series.empty:
                return False

        return all(type(v) is str for v in series)

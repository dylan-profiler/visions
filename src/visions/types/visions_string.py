import pandas as pd
import pandas.api.types as pdt
from typing import Sequence

from visions.relations import IdentityRelation, TypeRelation
from visions.types.type import VisionsBaseType


def _get_relations(cls) -> Sequence[TypeRelation]:
    from visions.types import visions_object

    relations = [IdentityRelation(cls, visions_object)]
    return relations


class visions_string(VisionsBaseType):
    """**String** implementation of :class:`visions.core.model.type.VisionsBaseType`.

    Examples:
        >>> x = pd.Series(['rubin', 'carter', 'champion'])
        >>> x in visions_string
        True
    """

    @classmethod
    def get_relations(cls) -> Sequence[TypeRelation]:
        return _get_relations(cls)

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

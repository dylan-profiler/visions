from typing import Sequence

import pandas as pd
import pandas.api.types as pdt

from visions.relations import IdentityRelation, TypeRelation
from visions.types.type import VisionsBaseType


def _get_relations(cls) -> Sequence[TypeRelation]:
    from visions.types import Object

    relations = [IdentityRelation(cls, Object)]
    return relations


def string_pandas_checker():
    if hasattr(pdt, 'is_string_dtype'):
        return pdt.is_string_dtype
    else:
        return pdt.is_object_dtype


string_check = string_pandas_checker()


class String(VisionsBaseType):
    """**String** implementation of :class:`visions.types.type.VisionsBaseType`.

    Examples:
        >>> x = pd.Series(['rubin', 'carter', 'champion'])
        >>> x in visions.String
        True
    """

    @classmethod
    def get_relations(cls) -> Sequence[TypeRelation]:
        return _get_relations(cls)

    @classmethod
    def contains_op(cls, series: pd.Series) -> bool:
        # TODO: without the object check this passes string categories... is there a better way?
        if not string_check(series) or pdt.is_categorical_dtype(series):
            return False

        if series.hasnans:
            series = series.dropna()
            if series.empty:
                return False

        return all(type(v) is str for v in series)

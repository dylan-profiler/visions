import pathlib
from typing import Sequence

import pandas as pd

from visions.relations import IdentityRelation, TypeRelation
from visions.types.type import VisionsBaseType
from visions.utils.series_utils import nullable_series_contains, series_not_empty


def _get_relations(cls) -> Sequence[TypeRelation]:
    from visions.types import Path

    relations = [IdentityRelation(cls, Path)]
    return relations


class File(VisionsBaseType):
    """**File** implementation of :class:`visions.types.type.VisionsBaseType`.
    (i.e. existing path)

    Examples:
        >>> x = pd.Series([pathlib.Path('/home/user/file.txt'), pathlib.Path('/home/user/test2.txt')])
        >>> x in visions.File
        True
    """

    @classmethod
    def get_relations(cls) -> Sequence[TypeRelation]:
        return _get_relations(cls)

    @classmethod
    @series_not_empty
    @nullable_series_contains
    def contains_op(cls, series: pd.Series, state: dict) -> bool:
        return all(isinstance(p, pathlib.Path) and p.exists() for p in series)

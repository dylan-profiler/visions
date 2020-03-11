from typing import Sequence

import pathlib
import pandas as pd

from visions.relations import IdentityRelation, TypeRelation
from visions.types import VisionsBaseType


def _get_relations(cls) -> Sequence[TypeRelation]:
    from visions.types import Path

    relations = [IdentityRelation(cls, Path)]
    return relations


class ExistingPath(VisionsBaseType):
    """**Existing Path** implementation of :class:`visions.types.type.VisionsBaseType`.

    Examples:
        >>> x = pd.Series([pathlib.Path('/home/user/file.txt'), pathlib.Path('/home/user/test2.txt')])
        >>> x in visions.ExistingPath
        True
    """

    @classmethod
    def get_relations(cls) -> Sequence[TypeRelation]:
        return _get_relations(cls)

    @classmethod
    def contains_op(cls, series: pd.Series) -> bool:
        return all(isinstance(p, pathlib.Path) and p.exists() for p in series)

import imghdr
from pathlib import Path
from typing import Sequence

import pandas as pd

from visions.relations import IdentityRelation, TypeRelation
from visions.types import VisionsBaseType


def _get_relations(cls) -> Sequence[TypeRelation]:
    from visions.types import ExistingPath

    relations = [IdentityRelation(cls, ExistingPath)]
    return relations


class ImagePath(VisionsBaseType):
    """**Image Path** implementation of :class:`visions.types.type.VisionsBaseType`.

    Examples:
        >>> x = pd.Series([Path('/home/user/file.png'), Path('/home/user/test2.jpg')])
        >>> x in visions.ImagePath
        True
    """

    @classmethod
    def get_relations(cls) -> Sequence[TypeRelation]:
        return _get_relations(cls)

    @classmethod
    def contains_op(cls, series: pd.Series) -> bool:
        return all(
            isinstance(p, Path) and p.exists() and imghdr.what(p) for p in series
        )

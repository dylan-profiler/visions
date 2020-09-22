import imghdr
from pathlib import Path
from typing import Sequence

import pandas as pd

from visions.relations import IdentityRelation, TypeRelation
from visions.types.type import VisionsBaseType
from visions.utils.series_utils import nullable_series_contains, series_not_empty


def _get_relations(cls) -> Sequence[TypeRelation]:
    from visions.types import File

    relations = [IdentityRelation(cls, File)]
    return relations


class Image(VisionsBaseType):
    """**Image** implementation of :class:`visions.types.type.VisionsBaseType`.
    (i.e. series with all image files)

    Examples:
        >>> x = pd.Series([Path('/home/user/file.png'), Path('/home/user/test2.jpg')])
        >>> x in visions.Image
        True
    """

    @classmethod
    def get_relations(cls) -> Sequence[TypeRelation]:
        return _get_relations(cls)

    @classmethod
    @series_not_empty
    @nullable_series_contains
    def contains_op(cls, series: pd.Series, state: dict) -> bool:
        return all(
            isinstance(p, Path) and p.exists() and imghdr.what(p) for p in series
        )

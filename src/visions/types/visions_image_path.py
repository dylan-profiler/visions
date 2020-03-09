import imghdr
from pathlib import Path
import pandas as pd
from typing import Sequence

from visions.relations import IdentityRelation, TypeRelation
from visions.types import VisionsBaseType


def _get_relations(cls) -> Sequence[TypeRelation]:
    from visions.types import visions_existing_path

    relations = [IdentityRelation(cls, visions_existing_path)]
    return relations


class visions_image_path(VisionsBaseType):
    """**Image Path** implementation of :class:`visions.core.model.type.VisionsBaseType`.

    Examples:
        >>> x = pd.Series([Path('/home/user/file.png'), Path('/home/user/test2.jpg')])
        >>> x in visions_image_path
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

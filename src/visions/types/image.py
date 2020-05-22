import imghdr
from pathlib import Path
from typing import Sequence

import pandas as pd

from visions.relations import IdentityRelation, TypeRelation, InferenceRelation
from visions.types.type import VisionsBaseType
from visions.dtypes.stringdtype_alias import create_alias


ImageDtype = create_alias("image")


def _get_relations(cls) -> Sequence[TypeRelation]:
    from visions.types import File, String

    relations = [
        IdentityRelation(cls, String),
        InferenceRelation(
            cls,
            File,
            relationship=lambda series: all(imghdr.what(p) for p in series),
            transformer=lambda series: series.astype("image"),
        ),
    ]
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
    def contains_op(cls, series: pd.Series) -> bool:
        return series.dtype == "image"

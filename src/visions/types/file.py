import os

import pathlib
from typing import Sequence

import pandas as pd

from visions.relations import IdentityRelation, TypeRelation, InferenceRelation
from visions.types.type import VisionsBaseType
from visions.dtypes.stringdtype_alias import create_alias


create_alias("file")


def _get_relations(cls) -> Sequence[TypeRelation]:
    from visions.types import Path, String

    relations = [
        IdentityRelation(cls, String),
        InferenceRelation(
            cls,
            Path,
            relationship=lambda series: all(os.path.exists(p) for p in series),
            transformer=lambda series: series.astype("file"),
        ),
    ]
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
    def contains_op(cls, series: pd.Series) -> bool:
        return series.dtype == "file"

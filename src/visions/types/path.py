import ntpath
import posixpath
import pathlib
from typing import Sequence

import pandas as pd

from visions.relations import IdentityRelation, InferenceRelation, TypeRelation
from visions.types.type import VisionsBaseType


def string_is_path(series) -> bool:
    try:
        return all(posixpath.isabs(x) for x in series) or all(
            ntpath.isabs(x) for x in series
        )
    except TypeError:
        return False


def to_path(series):
    return series.astype("path")


def _get_relations(cls) -> Sequence[TypeRelation]:
    from visions.types import String

    relations = [
        IdentityRelation(cls, String),
        InferenceRelation(
            cls, String, relationship=string_is_path, transformer=to_path
        ),
    ]
    return relations


class Path(VisionsBaseType):
    """**Path** implementation of :class:`visions.types.type.VisionsBaseType`.

    Examples:
        >>> import pathlib
        >>> x = pd.Series([pathlib.Path('/home/user/file.txt'), pathlib.Path('/home/user/test2.txt')])
        >>> x in visions.Path
        True
    """

    @classmethod
    def get_relations(cls) -> Sequence[TypeRelation]:
        return _get_relations(cls)

    @classmethod
    def contains_op(cls, series: pd.Series) -> bool:
        return series.dtype == "path"

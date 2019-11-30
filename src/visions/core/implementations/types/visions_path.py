from pathlib import Path, PureWindowsPath, PurePosixPath, PurePath
from typing import Sequence
import pandas as pd

from visions.core.model.relations import (
    IdentityRelation,
    InferenceRelation,
    TypeRelation,
)
from visions.core.model.type import VisionsBaseType


def string_is_path(series) -> bool:
    try:
        s = to_path(series.copy())
        return s.apply(lambda x: x.is_absolute()).all()
    except TypeError:
        return False


def to_path(series: pd.Series) -> pd.Series:
    s = series.copy().apply(PureWindowsPath)
    if not s.apply(lambda x: x.is_absolute()).all():
        return series.apply(PurePosixPath)
    else:
        return s


def _get_relations() -> Sequence[TypeRelation]:
    from visions.core.implementations.types import visions_object, visions_string

    relations = [
        IdentityRelation(visions_path, visions_object),
        InferenceRelation(
            visions_path,
            visions_string,
            relationship=string_is_path,
            transformer=to_path,
        ),
    ]
    return relations


class visions_path(VisionsBaseType):
    """**Path** implementation of :class:`visions.core.model.type.VisionsBaseType`.

    Examples:
        >>> x = pd.Series([Path('/home/user/file.txt'), Path('/home/user/test2.txt')])
        >>> x in visions_path
        True
    """

    @classmethod
    def get_relations(cls) -> Sequence[TypeRelation]:
        return _get_relations()

    @classmethod
    def contains_op(cls, series: pd.Series) -> bool:
        return all(isinstance(x, PurePath) and x.is_absolute() for x in series)

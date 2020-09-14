import pathlib
from typing import Sequence

import pandas as pd

from visions.relations import IdentityRelation, InferenceRelation, TypeRelation
from visions.types.type import VisionsBaseType
from visions.utils.series_utils import nullable_series_contains, series_not_empty


def string_is_path(series, state: dict) -> bool:
    try:
        s = to_path(series.copy(), state)
        return s.apply(lambda x: x.is_absolute()).all()
    except TypeError:
        return False


def to_path(series: pd.Series, state: dict) -> pd.Series:
    s = series.copy().apply(pathlib.PureWindowsPath)
    if not s.apply(lambda x: x.is_absolute()).all():
        return series.apply(pathlib.PurePosixPath)
    else:
        return s


def _get_relations(cls) -> Sequence[TypeRelation]:
    from visions.types import Object, String

    relations = [
        IdentityRelation(cls, Object),
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
    @series_not_empty
    @nullable_series_contains
    def contains_op(cls, series: pd.Series, state: dict) -> bool:
        return all(isinstance(x, pathlib.PurePath) and x.is_absolute() for x in series)

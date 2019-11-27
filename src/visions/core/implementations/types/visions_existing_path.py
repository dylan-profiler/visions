from pathlib import Path
import pandas as pd
from typing import Sequence

from visions.core.model.relations import (
    IdentityRelation,
    InferenceRelation,
    TypeRelation,
)
from visions.core.model.type import VisionsBaseType


def _get_relations() -> Sequence[TypeRelation]:
    from visions.core.implementations.types import visions_path

    relations = [IdentityRelation(visions_existing_path, visions_path)]
    return relations


class visions_existing_path(VisionsBaseType):
    """**Existing Path** implementation of :class:`visions.core.model.type.VisionsBaseType`.

    Examples:
        >>> x = pd.Series([Path('/home/user/file.txt'), Path('/home/user/test2.txt')])
        >>> x in visions_existing_path
        True
    """

    @classmethod
    def get_relations(cls) -> Sequence[TypeRelation]:
        return _get_relations()

    @classmethod
    def contains_op(cls, series: pd.Series) -> bool:
        return all(isinstance(p, Path) and p.exists() for p in series)

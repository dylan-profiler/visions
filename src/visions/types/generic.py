from typing import Iterable, Sequence

from visions.relations import TypeRelation
from visions.types.type import VisionsBaseType


class Generic(VisionsBaseType):
    """**Generic** implementation of :class:`visions.types.type.VisionsBaseType`.

    Examples:
        >>> import numpy as np
        >>> import visions
        >>> x = ['a', 1, np.nan]
        >>> x in visions.Generic
        True
    """

    @classmethod
    def get_relations(cls) -> Sequence[TypeRelation]:
        return []

    @classmethod
    def contains_op(cls, iterable: Iterable, state: dict) -> bool:
        return True

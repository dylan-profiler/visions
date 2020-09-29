from typing import Any, Sequence

from multimethod import multimethod

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

    @staticmethod
    @multimethod
    def contains_op(item: Any, state: dict) -> bool:
        return True

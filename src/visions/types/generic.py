from typing import Sequence

import pandas as pd

from visions.relations import TypeRelation
from visions.types.type import VisionsBaseType


class Generic(VisionsBaseType):
    """**Generic** implementation of :class:`visions.types.type.VisionsBaseType`.

    Examples:
        >>> import numpy as np
        >>> x = pd.Series(['a', 1, np.nan])
        >>> x in visions.Generic
        True
    """

    @classmethod
    def get_relations(cls) -> Sequence[TypeRelation]:
        return []

    @classmethod
    def contains_op(cls, series: pd.Series, state: dict) -> bool:
        return True

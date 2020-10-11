from typing import Sequence

import pandas as pd
from pandas.api import types as pdt

from visions.relations import IdentityRelation, TypeRelation
from visions.types.type import VisionsBaseType


class Sparse(VisionsBaseType):
    """**Sparse** implementation of :class:`visions.types.type.VisionsBaseType`.

    Examples:
        >>> import numpy as np
        >>> x = pd.Sparse(pd.Series([np.complex(0, 0), np.complex(1, 2), np.complex(3, -1), np.nan]))
        >>> x in visions.Sparse
        True
    """

    @classmethod
    def get_relations(cls) -> Sequence[TypeRelation]:
        from visions.types import Generic

        relations = [IdentityRelation(cls, Generic)]
        return relations

    @classmethod
    def contains_op(cls, series: pd.Series, state: dict) -> bool:
        return pdt.is_sparse(series)

from functools import singledispatch
from typing import Iterable, Sequence

from visions.relations import IdentityRelation, TypeRelation
from visions.types.type import VisionsBaseType


@singledispatch
def sparse_contains(sequence: Iterable, state: dict) -> bool:
    return False


class Sparse(VisionsBaseType):
    """**Sparse** implementation of :class:`visions.types.type.VisionsBaseType`.

    Examples:
        >>> import pandas as pd
        >>> import visions
        >>> x = pd.Sparse(pd.Series([np.complex(0, 0), np.complex(1, 2), np.complex(3, -1)]))
        >>> x in visions.Sparse
        True
    """

    @classmethod
    def get_relations(cls) -> Sequence[TypeRelation]:
        from visions.types import Generic

        relations = [IdentityRelation(cls, Generic)]
        return relations

    @classmethod
    def contains_op(cls, sequence: Iterable, state: dict) -> bool:
        return sparse_contains(sequence, state)


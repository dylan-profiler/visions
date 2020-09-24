import numbers
from functools import singledispatch
from typing import Iterable, Sequence

from visions.relations import IdentityRelation, TypeRelation
from visions.types.type import VisionsBaseType


@singledispatch
def numeric_contains_op(sequence: Iterable, state: dict):
    return all(
        isinstance(value, numbers.Number) and not isinstance(value, bool)
        for value in sequence
    )


class Numeric(VisionsBaseType):
    """**Numeric** implementation of :class:`visions.types.type.VisionsBaseType`.

    Examples:
        >>> import visions
        >>> from decimal import Decimal
        >>>
        >>> x = [Decimal(1), Decimal(2), Decimal(3)]
        >>> x in visions.Numeric
        True
    """

    @classmethod
    def get_relations(cls) -> Sequence[TypeRelation]:
        from visions import Generic

        relations = [IdentityRelation(cls, Generic)]
        return relations

    @classmethod
    def contains_op(cls, sequence: Iterable, state: dict) -> bool:
        return numeric_contains_op(sequence, state)

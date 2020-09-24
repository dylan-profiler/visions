from functools import singledispatch
from typing import Iterable, Sequence

from visions.backends.python.series_utils import sequence_not_empty
from visions.relations import IdentityRelation, InferenceRelation, TypeRelation
from visions.types.type import VisionsBaseType


@singledispatch
def float_to_int(sequence: Iterable, state: dict) -> Iterable:
    return map(int, sequence)


@singledispatch
def float_is_int(sequence: Iterable, state: dict) -> bool:
    try:
        return all(int(value) == value for value in sequence)
    except (ValueError, TypeError):
        return False


@singledispatch
@sequence_not_empty
def integer_contains(sequence: Iterable, state: dict) -> bool:
    return all(
        isinstance(value, int) and not isinstance(value, bool) for value in sequence
    )


class Integer(VisionsBaseType):
    """**Integer** implementation of :class:`visions.types.type.VisionsBaseType`.

    Examples:
        >>> import pandas as pd
        >>> x = [-1, 1, 2, 3]
        >>> x in visions.Integer
        True
    """

    @classmethod
    def get_relations(cls) -> Sequence[TypeRelation]:
        from visions.types import Float, Generic

        relations = [
            IdentityRelation(cls, Generic),
            InferenceRelation(
                cls, Float, relationship=float_is_int, transformer=float_to_int
            ),
        ]
        return relations

    @classmethod
    def contains_op(cls, sequence: Iterable, state: dict) -> bool:
        return integer_contains(sequence, state)

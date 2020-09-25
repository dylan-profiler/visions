from functools import singledispatch
from typing import Iterable, Sequence

from visions.backends.python.series_utils import sequence_not_empty
from visions.relations import IdentityRelation, InferenceRelation, TypeRelation
from visions.types.type import VisionsBaseType


def no_leading_zeros(sequence, coerced_sequence) -> bool:
    return not any(s[0] == "0" and c > 1 for s, c in zip(sequence, coerced_sequence))


@singledispatch
def string_to_float(sequence: Iterable, state: dict) -> Iterable:
    return map(float, sequence)


@singledispatch
def string_is_float(sequence: Iterable, state: dict) -> bool:
    try:
        coerced = list(string_to_float(sequence, state))
        return no_leading_zeros(sequence, coerced)
    except ValueError:
        return False


@singledispatch
def complex_to_float(sequence: Iterable, state: dict) -> Iterable:
    return map(lambda v: v.real, sequence)


@singledispatch
def complex_is_float(sequence: Iterable, state: dict) -> bool:
    try:
        return all(value.imag == 0 for value in sequence)
    except ValueError:
        return False


@singledispatch
@sequence_not_empty
def float_contains(sequence: Iterable, state: dict) -> bool:
    return all(isinstance(value, float) for value in sequence)


class Float(VisionsBaseType):
    """**Float** implementation of :class:`visions.types.type.VisionsBaseType`.

    Examples:
        >>> import visions
        >>> x = [1.0, 2.5, 5.0]
        >>> x in visions.Float
        True
    """

    @classmethod
    def get_relations(cls) -> Sequence[TypeRelation]:
        from visions.types import Complex, Generic, String

        relations = [
            IdentityRelation(cls, Generic),
            InferenceRelation(
                cls, String, relationship=string_is_float, transformer=string_to_float
            ),
            InferenceRelation(
                cls,
                Complex,
                relationship=complex_is_float,
                transformer=complex_to_float,
            ),
        ]
        return relations

    @classmethod
    def contains_op(cls, sequence: Iterable, state: dict) -> bool:
        return float_contains(sequence, state)

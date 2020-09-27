from functools import singledispatch
from typing import Iterable, Sequence

from visions.backends.python.series_utils import sequence_not_empty
from visions.relations import IdentityRelation, InferenceRelation, TypeRelation
from visions.types.float import no_leading_zeros
from visions.types.type import VisionsBaseType


@singledispatch
def string_is_complex(sequence: Iterable, state: dict) -> bool:
    try:
        coerced = list(string_to_complex(sequence, state))
        return no_leading_zeros(sequence, [r.real for r in coerced])
    except:
        return False


@singledispatch
def string_to_complex(sequence: Iterable, state: dict) -> Iterable:
    return list(map(complex, sequence))


@singledispatch
@sequence_not_empty
def complex_contains(sequence: Iterable, state: dict) -> bool:
    return all(isinstance(value, complex) for value in sequence)


class Complex(VisionsBaseType):
    """**Complex** implementation of :class:`visions.types.type.VisionsBaseType`.

    Examples:
        >>> x = [complex(0, 0), complex(1, 2), complex(3, -1)]
        >>> x in visions.Complex
        True
    """

    @classmethod
    def get_relations(cls) -> Sequence[TypeRelation]:
        from visions.types import Generic, String

        relations = [
            IdentityRelation(cls, Generic),
            InferenceRelation(
                cls,
                String,
                relationship=string_is_complex,
                transformer=string_to_complex,
            ),
        ]
        return relations

    @classmethod
    def contains_op(cls, sequence: Iterable, state: dict) -> bool:
        return complex_contains(sequence, state)

from typing import Sequence

from visions.backends.python.series_utils import sequence_not_empty
from visions.backends.python.types.float import no_leading_zeros
from visions.types.complex import Complex
from visions.types.string import String


@Complex.register_relationship(String, Sequence)
def string_is_complex(sequence: Sequence, state: dict) -> bool:
    try:
        coerced = list(string_to_complex(sequence, state))
        return no_leading_zeros(sequence, [r.real for r in coerced])
    except (ValueError, TypeError, AttributeError):
        return False


@Complex.register_transformer(String, Sequence)
def string_to_complex(sequence: Sequence, state: dict) -> Sequence:
    return list(map(complex, sequence))


@Complex.contains_op.register
@sequence_not_empty
def complex_contains(sequence: Sequence, state: dict) -> bool:
    return all(isinstance(value, complex) for value in sequence)

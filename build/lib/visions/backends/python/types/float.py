from typing import Sequence

from visions.backends.python.series_utils import sequence_not_empty
from visions.types.complex import Complex
from visions.types.float import Float
from visions.types.string import String


def no_leading_zeros(sequence, coerced_sequence) -> bool:
    return not any(s[0] == "0" and c > 1 for s, c in zip(sequence, coerced_sequence))


@Float.register_relationship(String, Sequence)
def string_is_float(sequence: Sequence, state: dict) -> bool:
    try:
        coerced = list(string_to_float(sequence, state))
        return no_leading_zeros(sequence, coerced)
    except ValueError:
        return False


@Float.register_transformer(String, Sequence)
def string_to_float(sequence: Sequence, state: dict) -> Sequence:
    return tuple(map(float, sequence))


@Float.register_relationship(Complex, Sequence)
def complex_is_float(sequence: Sequence, state: dict) -> bool:
    try:
        return all(value.imag == 0 for value in sequence)
    except ValueError:
        return False


@Float.register_transformer(Complex, Sequence)
def complex_to_float(sequence: Sequence, state: dict) -> Sequence:
    return list(map(lambda v: v.real, sequence))


@Float.contains_op.register
@sequence_not_empty
def float_contains(sequence: Sequence, state: dict) -> bool:
    return all(isinstance(value, float) for value in sequence)

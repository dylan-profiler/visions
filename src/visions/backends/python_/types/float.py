from typing import Iterable

from visions.types.complex import Complex
from visions.types.string import String
from visions.types.float import Float
from visions.backends.python_.series_utils import sequence_not_empty


def no_leading_zeros(sequence, coerced_sequence) -> bool:
    return not any(s[0] == "0" and c > 1 for s, c in zip(sequence, coerced_sequence))


@Float.register_relationship(String, Iterable)
def string_is_float(sequence: Iterable, state: dict) -> bool:
    try:
        coerced = list(string_to_float(sequence, state))
        return no_leading_zeros(sequence, coerced)
    except ValueError:
        return False


@Float.register_transformer(String, Iterable)
def string_to_float(sequence: Iterable, state: dict) -> Iterable:
    return map(float, sequence)


@Float.register_relationship(Complex, Iterable)
def complex_is_float(sequence: Iterable, state: dict) -> bool:
    try:
        return all(value.imag == 0 for value in sequence)
    except ValueError:
        return False


@Float.register_transformer(Complex, Iterable)
def complex_to_float(sequence: Iterable, state: dict) -> Iterable:
    return list(map(lambda v: v.real, sequence))


@Float.contains_op.register(Iterable)
@sequence_not_empty
def float_contains(sequence: Iterable, state: dict) -> bool:
    return all(isinstance(value, float) for value in sequence)

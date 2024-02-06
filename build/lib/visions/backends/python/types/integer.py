from typing import Sequence

from visions.backends.python.series_utils import sequence_not_empty
from visions.types.float import Float
from visions.types.integer import Integer


@Integer.register_relationship(Float, Sequence)
def float_is_int(sequence: Sequence, state: dict) -> bool:
    try:
        return all(int(value) == value for value in sequence)
    except (ValueError, TypeError, OverflowError):
        return False


@Integer.register_transformer(Float, Sequence)
def float_to_int(sequence: Sequence, state: dict) -> Sequence:
    return tuple(map(int, sequence))


@Integer.contains_op.register
@sequence_not_empty
def integer_contains(sequence: Sequence, state: dict) -> bool:
    return all(
        isinstance(value, int) and not isinstance(value, bool) for value in sequence
    )

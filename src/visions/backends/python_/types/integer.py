from typing import Iterable

from visions.types.float import Float
from visions.types.integer import Integer
from visions.backends.python_.series_utils import sequence_not_empty


@Integer.register_relationship(Float, Iterable)
def float_is_int(sequence: Iterable, state: dict) -> bool:
    try:
        return all(int(value) == value for value in sequence)
    except (ValueError, TypeError, OverflowError):
        return False


@Integer.register_transformer(Float, Iterable)
def float_to_int(sequence: Iterable, state: dict) -> Iterable:
    return map(int, sequence)


@Integer.contains_op.register(Iterable)
@sequence_not_empty
def integer_contains(sequence: Iterable, state: dict) -> bool:
    return all(
        isinstance(value, int) and not isinstance(value, bool) for value in sequence
    )

import numbers
from typing import Iterable

from visions.types.numeric import Numeric


@Numeric.contains_op.register(Iterable)
def numeric_contains_op(sequence: Iterable, state: dict):
    return all(
        isinstance(value, numbers.Number) and not isinstance(value, bool)
        for value in sequence
    )

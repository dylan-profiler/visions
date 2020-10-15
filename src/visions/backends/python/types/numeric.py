import numbers
from typing import Sequence

from visions.types.numeric import Numeric


@Numeric.contains_op.register
def numeric_contains_op(sequence: Sequence, state: dict):
    return all(
        isinstance(value, numbers.Number) and not isinstance(value, bool)
        for value in sequence
    )

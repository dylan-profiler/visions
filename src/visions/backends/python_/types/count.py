from typing import Sequence

from visions.types.count import Count


@Count.contains_op.register
def count_contains(sequence: Sequence, state: dict) -> bool:
    return all(isinstance(value, int) and value >= 0 for value in sequence)

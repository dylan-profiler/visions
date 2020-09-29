from typing import Iterable

from visions.types.count import Count


@Count.contains_op.register(Iterable)
def count_contains(sequence: Iterable, state: dict) -> bool:
    return all(isinstance(value, int) and value >= 0 for value in sequence)

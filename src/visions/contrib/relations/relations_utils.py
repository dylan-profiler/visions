from typing import Sequence


def values_are_consecutive(sequence: Sequence) -> bool:
    return sorted(sequence) == list(range(min(sequence), max(sequence) + 1))

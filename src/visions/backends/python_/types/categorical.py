from typing import Iterable

from visions.types.categorical import Categorical


@Categorical.contains_op.register(Iterable)
def categorical_contains(sequence: Iterable, state: dict) -> bool:
    return False

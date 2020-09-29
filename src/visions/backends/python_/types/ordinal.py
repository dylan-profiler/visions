from typing import Iterable

from visions.types.ordinal import Ordinal


@Ordinal.contains_op.register(Iterable)
def ordinal_contains(sequence: Iterable, state: dict) -> bool:
    return False

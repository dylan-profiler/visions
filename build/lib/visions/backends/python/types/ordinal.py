from typing import Sequence

from visions.types.ordinal import Ordinal


@Ordinal.contains_op.register
def ordinal_contains(sequence: Sequence, state: dict) -> bool:
    return False

from typing import Iterable

from visions.types.object import Object
from visions.backends.python_.series_utils import (
    sequence_handle_none,
    sequence_not_empty,
)


@Object.contains_op.register(Iterable)
@sequence_not_empty
@sequence_handle_none
def object_contains(sequence: Iterable, state: dict) -> bool:
    return any(not isinstance(value, (float, bool, int, complex)) for value in sequence)

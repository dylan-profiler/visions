from typing import Iterable

from visions.backends.python_.series_utils import (
    sequence_handle_none,
    sequence_not_empty,
)
from visions.types.string import String


@String.contains_op.register(Iterable)
@sequence_not_empty
@sequence_handle_none
def string_contains(sequence: Iterable, state: dict) -> bool:
    return all(isinstance(v, str) for v in sequence)

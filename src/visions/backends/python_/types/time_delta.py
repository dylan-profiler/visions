from datetime import timedelta
from typing import Iterable

from visions.types.time_delta import TimeDelta
from visions.backends.python_.series_utils import sequence_not_empty


@TimeDelta.contains_op.register(Iterable)
@sequence_not_empty
def time_delta_contains(sequence: Iterable, state: dict) -> bool:
    return all(isinstance(value, timedelta) for value in sequence)

from datetime import datetime
from typing import Sequence

from visions.backends.python.series_utils import sequence_not_empty
from visions.types.date_time import DateTime
from visions.types.string import String


@DateTime.register_relationship(String, Sequence)
def string_is_datetime(sequence: Sequence, state: dict) -> bool:
    try:
        _ = list(string_to_datetime(sequence, state))
        return True
    except (OverflowError, TypeError, ValueError):
        return False


@DateTime.register_transformer(String, Sequence)
def string_to_datetime(sequence: Sequence, state: dict) -> Sequence:
    """
    Python 3.7+
    return map(datetime.fromisoformat, sequence)
    """
    return tuple(map(lambda s: datetime.strptime(s, "%Y-%m-%d %H:%M:%S"), sequence))


@DateTime.contains_op.register
@sequence_not_empty
def datetime_contains(sequence: Sequence, state: dict) -> bool:
    return all(isinstance(value, datetime) for value in sequence)

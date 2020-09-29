from datetime import datetime
from typing import Iterable

from visions.backends.python_.series_utils import sequence_not_empty
from visions.types.date_time import DateTime
from visions.types.string import String


@DateTime.register_relationship(String, Iterable)
def string_is_datetime(sequence: Iterable, state: dict) -> bool:
    try:
        _ = list(string_to_datetime(sequence, state))
        return True
    except (OverflowError, TypeError, ValueError):
        return False


@DateTime.register_transformer(String, Iterable)
def string_to_datetime(sequence: Iterable, state: dict) -> Iterable:
    """
    Python 3.7+
    return map(datetime.fromisoformat, sequence)
    """
    return map(lambda s: datetime.strptime(s, "%Y-%m-%d %H:%M:%S"), sequence)


@DateTime.contains_op.register(Iterable)
@sequence_not_empty
def datetime_contains(sequence: Iterable, state: dict) -> bool:
    return all(isinstance(value, datetime) for value in sequence)

from datetime import date, time
from typing import Sequence

from visions.types.date import Date
from visions.types.date_time import DateTime


@Date.register_relationship(DateTime, Sequence)
def datetime_is_date(sequence: Sequence, state: dict) -> bool:
    value = time(0, 0)
    return all(v == value for v in sequence)


@Date.register_transformer(DateTime, Sequence)
def datetime_to_date(sequence: Sequence, state: dict) -> Sequence:
    return tuple(map(lambda v: v.date(), sequence))


@Date.contains_op.register
def date_contains(sequence: Sequence, state: dict) -> bool:
    return all(isinstance(value, date) for value in sequence)

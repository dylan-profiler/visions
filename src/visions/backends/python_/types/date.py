from datetime import date, time
from typing import Iterable

from visions.types.date import Date
from visions.types.date_time import DateTime


@Date.register_relationship(DateTime, Iterable)
def datetime_is_date(sequence: Iterable, state: dict) -> bool:
    value = time(0, 0)
    return all(v == value for v in sequence)


@Date.register_transformer(DateTime, Iterable)
def datetime_to_date(sequence: Iterable, state: dict) -> Iterable:
    return map(lambda v: v.date(), sequence)


@Date.contains_op.register(Iterable)
def date_contains(sequence: Iterable, state: dict) -> bool:
    return all(isinstance(value, date) for value in sequence)

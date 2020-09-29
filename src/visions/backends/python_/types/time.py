from datetime import date, time
from typing import Iterable

from visions.types.date_time import DateTime
from visions.types.time import Time


# @Time.register_relationship(DateTime, Iterable)
# def datetime_is_time(sequence: Iterable, state: dict) -> bool:
#     value = date(1, 1, 1)
#     return all(v == value for v in sequence)
#
#
# @Time.register_transformer(DateTime, Iterable)
# def datetime_to_time(sequence: Iterable, state: dict) -> Iterable:
#     return map(lambda v: v.time(), sequence)


@Time.contains_op.register()
def time_contains(sequence: Iterable, state: dict) -> bool:
    return all(isinstance(value, time) for value in sequence)

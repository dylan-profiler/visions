from datetime import time
from typing import Sequence

# from visions.types.date_time import DateTime
from visions.types.time import Time

# @Time.register_relationship(DateTime, Sequence)
# def datetime_is_time(sequence: Sequence, state: dict) -> bool:
#     value = date(1, 1, 1)
#     return all(v == value for v in sequence)
#
#
# @Time.register_transformer(DateTime, Sequence)
# def datetime_to_time(sequence: Sequence, state: dict) -> Sequence:
#     return map(lambda v: v.time(), sequence)


@Time.contains_op.register
def time_contains(sequence: Sequence, state: dict) -> bool:
    return all(isinstance(value, time) for value in sequence)

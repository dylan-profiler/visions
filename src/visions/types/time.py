from datetime import date, time
from functools import singledispatch
from typing import Iterable, Sequence

from visions.relations import IdentityRelation, TypeRelation
from visions.types.type import VisionsBaseType


@singledispatch
def datetime_is_time(sequence: Iterable, state: dict) -> bool:
    value = date(1, 1, 1)
    return all(v == value for v in sequence)


@singledispatch
def datetime_to_time(sequence: Iterable, state: dict) -> Iterable:
    return map(lambda v: v.time(), sequence)


@singledispatch
def time_contains(sequence: Iterable, state: dict) -> bool:
    return all(isinstance(value, time) for value in sequence)


class Time(VisionsBaseType):
    """**Time** implementation of :class:`visions.types.type.VisionsBaseType`.

    Examples:
        >>> import datetime
        >>> import visions
        >>> x = [datetime.time(10, 8, 4), datetime.time(21, 17, 0)]
        >>> x in visions.Time
        True
    """

    @classmethod
    def get_relations(cls) -> Sequence[TypeRelation]:
        from visions.types import Object

        relations = [IdentityRelation(cls, Object)]
        return relations

    @classmethod
    def contains_op(cls, sequence: Iterable, state: dict) -> bool:
        return time_contains(sequence, state)

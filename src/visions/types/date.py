from datetime import date, time
from functools import singledispatch
from typing import Iterable, Sequence

from visions.relations import IdentityRelation, InferenceRelation, TypeRelation
from visions.types.type import VisionsBaseType


@singledispatch
def datetime_is_date(sequence: Iterable, state: dict) -> bool:
    value = time(0, 0)
    return all(v == value for v in sequence)


@singledispatch
def datetime_to_date(sequence: Iterable, state: dict) -> Iterable:
    return map(lambda v: v.date(), sequence)


@singledispatch
def date_contains(sequence: Iterable, state: dict) -> bool:
    return all(isinstance(value, date) for value in sequence)


class Date(VisionsBaseType):
    """**Date** implementation of :class:`visions.types.type.VisionsBaseType`.
    All values are should be datetime.date or missing

    Examples:
        >>> import datetime
        >>> import visions
        >>> x = [datetime.date(2017, 3, 5), datetime.date(2019, 12, 4)]
        >>> x in visions.Date
        True
    """

    @classmethod
    def get_relations(cls) -> Sequence[TypeRelation]:
        from visions.types import DateTime, Object

        relations = [
            IdentityRelation(cls, Object),
            InferenceRelation(
                cls,
                DateTime,
                relationship=datetime_is_date,
                transformer=datetime_to_date,
            ),
        ]
        return relations

    @classmethod
    def contains_op(cls, sequence: Iterable, state: dict) -> bool:
        return date_contains(sequence, state)

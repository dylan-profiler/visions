from datetime import datetime
from functools import singledispatch
from typing import Iterable, Sequence

from visions.backends.python.series_utils import sequence_not_empty
from visions.relations import IdentityRelation, InferenceRelation, TypeRelation
from visions.types.type import VisionsBaseType


@singledispatch
def string_is_datetime(sequence: Iterable, state: dict) -> bool:
    try:
        _ = list(string_to_datetime(sequence, state))
        return True
    except (OverflowError, TypeError, ValueError):
        return False


@singledispatch
def string_to_datetime(sequence: Iterable, state: dict) -> Iterable:
    return map(datetime.fromisoformat, sequence)


@singledispatch
@sequence_not_empty
def datetime_contains(sequence: Iterable, state: dict) -> bool:
    return all(isinstance(value, datetime) for value in sequence)


class DateTime(VisionsBaseType):
    """**Datetime** implementation of :class:`visions.types.type.VisionsBaseType`.

    Examples:
        >>> import datetime
        >>> import visions
        >>> x = [datetime.datetime(2017, 3, 5), datetime.datetime(2019, 12, 4)]
        >>> x in visions.DateTime
        True
    """

    @classmethod
    def get_relations(cls) -> Sequence[TypeRelation]:
        from visions.types import Generic, String

        relations = [
            IdentityRelation(cls, Generic),
            InferenceRelation(
                cls,
                String,
                relationship=string_is_datetime,
                transformer=string_to_datetime,
            ),
        ]
        return relations

    @classmethod
    def contains_op(cls, sequence: Iterable, state: dict) -> bool:
        return datetime_contains(sequence, state)

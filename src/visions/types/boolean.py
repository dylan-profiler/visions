from functools import singledispatch
from typing import Iterable, Sequence

from visions.backends.python.series_utils import (
    sequence_handle_none,
    sequence_not_empty,
)
from visions.relations import IdentityRelation, InferenceRelation, TypeRelation
from visions.types.type import VisionsBaseType


@sequence_not_empty
@sequence_handle_none
def is_bool(sequence: Iterable, state: dict):
    return all(isinstance(value, bool) for value in sequence)


def to_bool(sequence: Iterable, state: dict):
    return map(bool, sequence)


@singledispatch
def object_to_bool(sequence: Iterable, state: dict) -> Iterable:
    return to_bool(sequence, state)


@singledispatch
def object_is_bool(sequence: Iterable, state: dict) -> bool:
    return is_bool(sequence, state)


@singledispatch
@sequence_handle_none
def string_is_bool(sequence: Iterable, state: dict):
    return all(value in ["True", "False"] for value in sequence)


@singledispatch
def string_to_bool(sequence: Iterable, state: dict):
    return map(lambda v: v == "True", sequence)


@singledispatch
def boolean_contains(sequence: Iterable, state: dict) -> bool:
    return is_bool(sequence, state)


class Boolean(VisionsBaseType):
    """**Boolean** implementation of :class:`visions.types.type.VisionsBaseType`.

    Examples:
        >>> import visions
        >>> x = [True, False, False, True]
        >>> x in visions.Boolean
        True

        >>> x = [True, False, None]
        >>> x in visions.Boolean
        True
    """

    @classmethod
    def get_relations(cls) -> Sequence[TypeRelation]:
        from visions.types import Generic, Object, String

        relations = [
            IdentityRelation(cls, Generic),
            InferenceRelation(
                cls,
                String,
                relationship=string_is_bool,
                transformer=string_to_bool,
            ),
            InferenceRelation(
                cls, Object, relationship=object_is_bool, transformer=object_to_bool
            ),
        ]
        return relations

    @classmethod
    def contains_op(cls, sequence: Iterable, state: dict) -> bool:
        return boolean_contains(sequence, state)

from typing import Iterable

from visions.backends.python_.series_utils import (
    sequence_handle_none,
    sequence_not_empty,
)
from visions.types import Boolean, Object, String


@sequence_not_empty
@sequence_handle_none
def is_bool(sequence: Iterable, state: dict):
    return all(isinstance(value, bool) for value in sequence)


def to_bool(sequence: Iterable, state: dict):
    return map(bool, sequence)


@Boolean.register_relationship(Object, Iterable)
def object_is_bool(sequence: Iterable, state: dict) -> bool:
    return is_bool(sequence, state)


@Boolean.register_transformer(Object, Iterable)
def object_to_bool(sequence: Iterable, state: dict) -> Iterable:
    return to_bool(sequence, state)


@Boolean.register_relationship(String, Iterable)
@sequence_handle_none
def string_is_bool(sequence: Iterable, state: dict):
    return all(value in ["True", "False"] for value in sequence)


@Boolean.register_transformer(String, Iterable)
def string_to_bool(sequence: Iterable, state: dict):
    return map(lambda v: v == "True", sequence)


@Boolean.contains_op.register(Iterable)
def boolean_contains(sequence: Iterable, state: dict) -> bool:
    print("!")
    return is_bool(sequence, state)

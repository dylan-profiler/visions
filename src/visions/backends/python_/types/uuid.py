import uuid
from typing import Sequence, Iterable

from visions.types.uuid import UUID
from visions.types.string import String


@UUID.contains_op.register
def uuid_contains(sequence: Iterable, state: dict) -> bool:
    return all(isinstance(value, uuid.UUID) for value in sequence)


@UUID.register_transformer(String, Iterable)
def string_to_uuid(sequence: Iterable, state: dict) -> Sequence:
    return [uuid.UUID(value) for value in sequence]


@UUID.register_relationship(String, Iterable)
def string_is_uuid(sequence: Iterable, state: dict) -> bool:
    try:
        string_to_uuid(sequence)
        return True
    except:
        return False

import uuid
from typing import Sequence

from visions.types.string import String
from visions.types.uuid import UUID


@UUID.contains_op.register
def uuid_contains(sequence: Sequence, state: dict) -> bool:
    return all(isinstance(value, uuid.UUID) for value in sequence)


@UUID.register_transformer(String, Sequence)
def string_to_uuid(sequence: Sequence, state: dict) -> Sequence:
    return [uuid.UUID(value) for value in sequence]


@UUID.register_relationship(String, Sequence)
def string_is_uuid(sequence: Sequence, state: dict) -> bool:
    try:
        string_to_uuid(sequence)
        return True
    except (ValueError, TypeError, AttributeError):
        return False

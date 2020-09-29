from typing import Sequence

from visions.types.email_address import FQDA, EmailAddress, _to_email
from visions.types.string import String


@EmailAddress.register_relationship(String, Sequence)
def string_is_email(sequence: Sequence, state: dict) -> bool:
    try:
        return all(
            value.local and value.fqdn for value in string_to_email(sequence, state)
        )
    except (ValueError, TypeError, AttributeError):
        return False


@EmailAddress.register_relationship(String, Sequence)
def string_to_email(sequence: Sequence, state: dict) -> Sequence:
    return tuple(map(_to_email, sequence))


@EmailAddress.contains_op.register
def email_address_contains(sequence: Sequence, state: dict) -> bool:
    return all(isinstance(value, FQDA) for value in sequence)

from typing import Iterable

from visions.types.string import String
from visions.types.email_address import FQDA, _to_email, EmailAddress


@EmailAddress.register_relationship(String, Iterable)
def string_is_email(sequence: Iterable, state: dict) -> bool:
    try:
        return all(
            value.local and value.fqdn for value in string_to_email(sequence, state)
        )
    except (ValueError, TypeError, AttributeError):
        return False


@EmailAddress.register_relationship(String, Iterable)
def string_to_email(sequence: Iterable, state: dict) -> Iterable:
    return map(_to_email, sequence)


@EmailAddress.contains_op.register(Iterable)
def email_address_contains(sequence: Iterable, state: dict) -> bool:
    return all(isinstance(value, FQDA) for value in sequence)

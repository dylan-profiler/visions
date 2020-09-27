from functools import singledispatch
from typing import Iterable, Sequence

import attr

from visions.relations import IdentityRelation, InferenceRelation, TypeRelation
from visions.types.type import VisionsBaseType


@attr.s(slots=True)
class FQDA(object):
    local = attr.ib()
    fqdn = attr.ib()

    @staticmethod
    def from_str(s):
        return _to_email(s)


def _to_email(s) -> FQDA:
    if isinstance(s, FQDA):
        return s
    elif isinstance(s, str):
        return FQDA(*s.split("@", maxsplit=1))
    else:
        raise TypeError("Only strings supported")


@singledispatch
def string_is_email(sequence: Iterable, state: dict) -> bool:
    try:
        return all(
            value.local and value.fqdn for value in string_to_email(sequence, state)
        )
    except (ValueError, TypeError, AttributeError):
        return False


@singledispatch
def string_to_email(sequence: Iterable, state: dict) -> Iterable:
    return map(_to_email, sequence)


@singledispatch
def email_address_contains(sequence: Iterable, state: dict) -> bool:
    return all(isinstance(value, FQDA) for value in sequence)


class EmailAddress(VisionsBaseType):
    """**EmailAddress** implementation of :class:`visions.types.type.VisionsBaseType`.

    Notes:
        The email address should be a **fully qualified domain address** (FQDA)
        FQDA = local part + @ + fully qualified domain name (FQDN)
        This type

    Examples:
        >>> import visions
        >>> x = [FQDA('example','gmail.com'), FQDA.from_str('example@protonmail.com')]
        >>> x in visions.EmailAddress
        True
    """

    @classmethod
    def get_relations(cls) -> Sequence[TypeRelation]:
        from visions.types import Object, String

        relations = [
            IdentityRelation(cls, Object),
            InferenceRelation(
                cls,
                String,
                relationship=string_is_email,
                transformer=string_to_email,
            ),
        ]
        return relations

    @classmethod
    def contains_op(cls, sequence: Iterable, state: dict) -> bool:
        return email_address_contains(sequence, state)

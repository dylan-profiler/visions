from functools import singledispatch
from ipaddress import _BaseAddress, ip_address
from typing import Iterable, Sequence

from visions.relations import IdentityRelation, InferenceRelation, TypeRelation
from visions.types.type import VisionsBaseType


@singledispatch
def string_is_ip_address(sequence: Iterable, state: dict) -> bool:
    try:
        _ = list(string_is_ip_address(sequence, state))
        return True
    except (ValueError, TypeError, AttributeError):
        return False


@singledispatch
def string_to_ip_address(sequence: Iterable, state: dict) -> Iterable:
    return map(ip_address, sequence)


@singledispatch
def ip_address_contains(sequence: Iterable, state: dict) -> bool:
    return all(isinstance(x, _BaseAddress) for x in sequence)


class IPAddress(VisionsBaseType):
    """**IP Address** (v4 and v6) implementation of :class:`visions.types.type.VisionsBaseType`.

    Examples:
        >>> from ipaddress import IPv4Address
        >>> import visions
        >>> x = [IPv4Address('127.0.0.1'), IPv4Address('128.0.1.2')]
        >>> x in visions.IPAddress
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
                relationship=string_is_ip_address,
                transformer=string_to_ip_address,
            ),
        ]
        return relations

    @classmethod
    def contains_op(cls, sequence: Iterable, state: dict) -> bool:
        return ip_address_contains(sequence, state)

from ipaddress import _BaseAddress, ip_address
from typing import Sequence

from visions.types.ip_address import IPAddress
from visions.types.string import String


@IPAddress.register_relationship(String, Sequence)
def string_is_ip_address(sequence: Sequence, state: dict) -> bool:
    try:
        _ = list(string_to_ip_address(sequence, state))
        return True
    except (ValueError, TypeError, AttributeError):
        return False


@IPAddress.register_transformer(String, Sequence)
def string_to_ip_address(sequence: Sequence, state: dict) -> Sequence:
    return tuple(map(ip_address, sequence))


@IPAddress.contains_op.register
def ip_address_contains(sequence: Sequence, state: dict) -> bool:
    return all(isinstance(x, _BaseAddress) for x in sequence)

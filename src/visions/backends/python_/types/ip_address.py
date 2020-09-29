from ipaddress import _BaseAddress, ip_address
from typing import Iterable

from visions.types.ip_address import IPAddress
from visions.types.string import String


@IPAddress.register_relationship(String, Iterable)
def string_is_ip_address(sequence: Iterable, state: dict) -> bool:
    try:
        _ = list(string_to_ip_address(sequence, state))
        return True
    except (ValueError, TypeError, AttributeError):
        return False


@IPAddress.register_transformer(String, Iterable)
def string_to_ip_address(sequence: Iterable, state: dict) -> Iterable:
    return map(ip_address, sequence)


@IPAddress.contains_op.register(Iterable)
def ip_address_contains(sequence: Iterable, state: dict) -> bool:
    return all(isinstance(x, _BaseAddress) for x in sequence)

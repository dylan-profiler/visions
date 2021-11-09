from typing import Sequence
from urllib.parse import ParseResult, urlparse

from visions.types.string import String
from visions.types.url import URL


@URL.contains_op.register
def url_contains(sequence: Sequence, state: dict) -> bool:
    return all(isinstance(value, ParseResult) for value in sequence)


@URL.register_transformer(String, Sequence)
def string_to_url(sequence: Sequence, state: dict) -> Sequence:
    return tuple(map(urlparse, sequence))


@URL.register_relationship(String, Sequence)
def string_is_url(sequence: Sequence, state: dict) -> bool:
    try:
        return all(x.netloc and x.scheme for x in string_to_url(sequence, {}))
    except (ValueError, TypeError, AttributeError):
        return False

from functools import singledispatch
from typing import Iterable, Sequence
from urllib.parse import ParseResult, urlparse

from visions.relations import IdentityRelation, InferenceRelation, TypeRelation
from visions.types.type import VisionsBaseType


@singledispatch
def string_is_url(sequence: Iterable, state: dict) -> bool:
    try:
        _ = all(isinstance(urlparse(value), ParseResult) for value in sequence)
        return True
    except:
        return False


@singledispatch
def string_to_url(sequence: Iterable, state: dict) -> Iterable:
    return map(urlparse, sequence)


@singledispatch
def url_contains(sequence: Iterable, state: dict) -> bool:
    return all(isinstance(sequence, ParseResult) for value in sequence)


class URL(VisionsBaseType):
    """**Url** implementation of :class:`visions.types.type.VisionsBaseType`.

    Examples:
        >>> from urllib.parse import urlparse
        >>> urls = ['http://www.cwi.nl:80/%7Eguido/Python.html', 'https://github.com/pandas-profiling/pandas-profiling']
        >>> x = [urlparse(url) for url in urls]
        >>> x in visions.URL
        True
    """

    @classmethod
    def get_relations(cls) -> Sequence[TypeRelation]:
        from visions.types import Object, String

        relations = [
            IdentityRelation(cls, Object),
            InferenceRelation(
                cls, String, relationship=string_is_url, transformer=string_to_url
            ),
        ]
        return relations

    @classmethod
    def contains_op(cls, sequence: Iterable, state: dict) -> bool:
        return url_contains(sequence, state)

from typing import Sequence
from urllib.parse import ParseResult, urlparse

import pandas as pd

from visions.relations import IdentityRelation, InferenceRelation, TypeRelation
from visions.types.type import VisionsBaseType
from visions.utils.series_utils import (
    func_nullable_series_contains,
    isinstance_attrs,
    nullable_series_contains,
    series_not_empty,
)


@func_nullable_series_contains
def string_is_url(series, state: dict) -> bool:
    try:
        return to_url(series, state).apply(lambda x: x.netloc and x.scheme).all()
    except AttributeError:
        return False


def to_url(series: pd.Series, state: dict) -> pd.Series:
    return series.apply(urlparse)


def _get_relations(cls) -> Sequence[TypeRelation]:
    from visions.types import Object, String

    relations = [
        IdentityRelation(cls, Object),
        InferenceRelation(cls, String, relationship=string_is_url, transformer=to_url),
    ]
    return relations


class URL(VisionsBaseType):
    """**Url** implementation of :class:`visions.types.type.VisionsBaseType`.

    Examples:
        >>> import pandas as pd
        >>> from urllib.parse import urlparse
        >>> urls = ['http://www.cwi.nl:80/%7Eguido/Python.html', 'https://github.com/pandas-profiling/pandas-profiling']
        >>> x = pd.Series([urlparse(url) for url in urls])
        >>> x in visions.URL
        True
    """

    @classmethod
    def get_relations(cls) -> Sequence[TypeRelation]:
        return _get_relations(cls)

    @classmethod
    @series_not_empty
    @nullable_series_contains
    def contains_op(cls, series: pd.Series, state: dict) -> bool:
        return isinstance_attrs(series, ParseResult, ["netloc", "scheme"])

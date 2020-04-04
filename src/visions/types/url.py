from typing import Sequence
from urllib.parse import urlparse, ParseResult

import pandas as pd

from visions.relations import IdentityRelation, InferenceRelation, TypeRelation
from visions.types.type import VisionsBaseType
from visions.utils.series_utils import nullable_series_contains


def test_url(series) -> bool:
    try:
        return to_url(series).apply(lambda x: all((x.netloc, x.scheme))).all()
    except AttributeError:
        return False


def to_url(series: pd.Series) -> pd.Series:
    return series.apply(urlparse)


def _get_relations(cls) -> Sequence[TypeRelation]:
    from visions.types import String, Object

    relations = [
        IdentityRelation(cls, Object),
        InferenceRelation(cls, String, relationship=test_url, transformer=to_url),
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
    @nullable_series_contains
    def contains_op(cls, series: pd.Series) -> bool:
        return all(
            isinstance(x, ParseResult) and all((x.netloc, x.scheme)) for x in series
        )

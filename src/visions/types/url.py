from typing import Sequence
from urllib.parse import ParseResult, urlparse

import pandas as pd

from visions.relations import IdentityRelation, InferenceRelation, TypeRelation
from visions.types.type import VisionsBaseType
from visions.dtypes.stringdtype_alias import create_alias


UrlDtype = create_alias("url")


def test_url(series) -> bool:
    try:
        return all(urlparse(x) and x.netloc and x.scheme for x in series)
    except AttributeError:
        return False


def to_url(series: pd.Series) -> pd.Series:
    return series.astype("url")


def _get_relations(cls) -> Sequence[TypeRelation]:
    from visions.types import String

    relations = [
        IdentityRelation(cls, String),
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
    def contains_op(cls, series: pd.Series) -> bool:
        return series.dtype == "url"

import pandas as pd
from urllib.parse import urlparse, ParseResult

from visions.core.model.relations import IdentityRelation, InferenceRelation
from visions.core.model.type import VisionsBaseType


def test_url(series):
    try:
        return to_url(series).apply(lambda x: all((x.netloc, x.scheme))).all()
    except AttributeError:
        return False


def to_url(series: pd.Series) -> pd.Series:
    return series.apply(urlparse)


def _get_relations():
    from visions.core.implementations.types import visions_string, visions_object

    relations = [
        IdentityRelation(visions_url, visions_object),
        InferenceRelation(
            visions_url, visions_string, relationship=test_url, transformer=to_url
        ),
    ]
    return relations


class visions_url(VisionsBaseType):
    """**Url** implementation of :class:`visions.core.model.type.VisionsBaseType`.

    Examples:
        >>> import pandas as pd
        >>> from urllib.parse import urlparse
        >>> urls = ['http://www.cwi.nl:80/%7Eguido/Python.html', 'https://github.com/pandas-profiling/pandas-profiling']
        >>> x = pd.Series([urlparse(url) for url in urls])
        >>> x in visions_url
        True
    """

    @classmethod
    def get_relations(cls):
        return _get_relations()

    @classmethod
    def contains_op(cls, series: pd.Series) -> bool:
        return all(
            isinstance(x, ParseResult) and all((x.netloc, x.scheme)) for x in series
        )

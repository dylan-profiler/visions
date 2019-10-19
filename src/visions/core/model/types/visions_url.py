import pandas as pd
from urllib.parse import urlparse, ParseResult

from visions.core.model.model_relation import relation_conf
from visions.core.model.models import VisionsBaseType


def test_url(series):
    try:
        return to_url(series).apply(lambda x: all((x.netloc, x.scheme))).all()
    except AttributeError:
        return False


def to_url(series: pd.Series) -> pd.Series:
    return series.apply(urlparse)


class visions_url(VisionsBaseType):
    """**Url** implementation of :class:`visions.core.models.VisionsBaseType`.

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
        from visions.core.model.types import visions_string, visions_object

        relations = {
            # TODO: replace test_url with coercion test
            visions_string: relation_conf(
                relationship=test_url, transformer=to_url, inferential=True
            ),
            visions_object: relation_conf(inferential=False),
        }
        return relations

    @classmethod
    def contains_op(cls, series: pd.Series) -> bool:
        return all(isinstance(x, ParseResult) and all((x.netloc, x.scheme))
                   for x in series)

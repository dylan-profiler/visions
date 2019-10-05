import pandas as pd
from urllib.parse import urlparse, ParseResult

from tenzing.core.model.model_relation import relation_conf
from tenzing.core.model.models import tenzing_model


class tenzing_url(tenzing_model):
    """**Url** implementation of :class:`tenzing.core.models.tenzing_model`.

    >>> from urllib.parse import urlparse
    >>> x = pd.Series([urlparse('http://www.cwi.nl:80/%7Eguido/Python.html'), urlparse('https://github.com/pandas-profiling/pandas-profiling')])
    >>> x in tenzing_url
    True
    """

    @classmethod
    def get_relations(cls):
        def test_url(series):
            try:
                return (
                    series.apply(urlparse).apply(lambda x: all((x.netloc, x.scheme))).all()
                )
            except AttributeError:
                return False

        from tenzing.core.model.types import tenzing_string
        from tenzing.core.model.types import tenzing_object
        relations = {
            # TODO: replace test_url with coerce url.cast + url.contains
            tenzing_string: relation_conf(relationship=test_url, inferential=True),
            tenzing_object: relation_conf(inferential=False),
        }
        return relations

    @classmethod
    def contains_op(cls, series: pd.Series) -> bool:
        return series.apply(lambda x: isinstance(x, ParseResult) and all((x.netloc, x.scheme))).all()

    @classmethod
    def cast_op(cls, series: pd.Series, operation=None) -> pd.Series:
        return series.apply(urlparse)

import pandas as pd
from urllib.parse import urlparse, ParseResult

from tenzing.core.models import tenzing_model


class tenzing_url(tenzing_model):
    """**Url** implementation of :class:`tenzing.core.models.tenzing_model`.

    >>> from urllib.parse import urlparse
    >>> x = pd.Series([urlparse('http://www.cwi.nl:80/%7Eguido/Python.html'), urlparse('https://github.com/pandas-profiling/pandas-profiling')])
    >>> x in tenzing_url
    True
    """

    @classmethod
    def contains_op(cls, series: pd.Series) -> bool:
        return series.apply(lambda x: isinstance(x, ParseResult)).all()

    @classmethod
    def cast_op(cls, series: pd.Series, operation=None) -> pd.Series:
        return series.apply(urlparse)

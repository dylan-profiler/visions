import pandas as pd
from urllib.parse import urlparse, ParseResult

from tenzing.core.model.types.tenzing_object import tenzing_object


class tenzing_url(tenzing_object):
    """**Path** implementation of :class:`tenzing.core.models.tenzing_model`.

    >>> from urllib.parse import urlparse
    >>> x = pd.Series([urlparse('http://www.cwi.nl:80/%7Eguido/Python.html'), urlparse('https://github.com/pandas-profiling/pandas-profiling')])
    >>> x in tenzing_url
    True
    """

    @classmethod
    def contains_op(cls, series):
        if not super().contains_op(series):
            return False

        return series.apply(lambda x: isinstance(x, ParseResult)).all()

    @classmethod
    def cast_op(cls, series, operation=None):
        return series.apply(urlparse)

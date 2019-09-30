import pandas as pd
from urllib.parse import urlparse

from tenzing.core.model.models import tenzing_model


class tenzing_url(tenzing_model):
    """**Url** implementation of :class:`tenzing.core.models.tenzing_model`.

    >>> from urllib.parse import urlparse
    >>> x = pd.Series([urlparse('http://www.cwi.nl:80/%7Eguido/Python.html'), urlparse('https://github.com/pandas-profiling/pandas-profiling')], dtype='Url')
    >>> x in tenzing_url
    True
    """

    @classmethod
    def contains_op(cls, series: pd.Series) -> bool:
        return series.dtype == "Url"

    @classmethod
    def cast_op(cls, series: pd.Series, operation=None) -> pd.Series:
        return series.astype("Url")

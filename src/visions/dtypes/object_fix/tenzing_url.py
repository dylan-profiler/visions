import pandas as pd
from urllib.parse import urlparse

from visions.core.model.type import VisionsBaseType


class visions_url(VisionsBaseType):
    """**Url** implementation of :class:`visions.core.models.VisionsBaseType`.

    >>> from urllib.parse import urlparse
    >>> x = pd.Series([urlparse('http://www.cwi.nl:80/%7Eguido/Python.html'), urlparse('https://github.com/pandas-profiling/pandas-profiling')], dtype='Url')
    >>> x in visions_url
    True
    """

    @classmethod
    def contains_op(cls, series: pd.Series) -> bool:
        return series.dtype == "Url"

    @classmethod
    def cast_op(cls, series: pd.Series, operation=None) -> pd.Series:
        return series.astype("Url")

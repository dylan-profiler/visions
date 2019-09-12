import pandas as pd
from urllib.parse import urlparse, ParseResult

import pandas.api.types as pdt

from tenzing.core.model_implementations.types.tenzing_object import tenzing_object
from tenzing.core.reuse import unique_summary


class tenzing_url(tenzing_object):
    """**Path** implementation of :class:`tenzing.core.models.tenzing_model`.

    >>> from urllib.parse import urlparse
    >>> x = pd.Series([urlparse('http://www.cwi.nl:80/%7Eguido/Python.html'), urlparse('https://github.com/pandas-profiling/pandas-profiling')])
    >>> x in tenzing_url
    True
    """

    @classmethod
    def contains_op(cls, series):
        # TODO: super()
        if not pdt.is_object_dtype(series):
            return False

        return series.apply(lambda x: isinstance(x, ParseResult)).all()

    @classmethod
    def cast_op(cls, series, operation=None):
        return series.apply(urlparse)

    @classmethod
    @unique_summary
    def summarization_op(cls, series):
        summary = super().summarization_op(series)

        keys = ["scheme", "netloc", "path", "query", "fragment"]
        url_parts = dict(zip(keys, zip(*series)))
        for name, part in url_parts.items():
            summary["{}_counts".format(name.lower())] = (
                pd.Series(part).value_counts().to_dict()
            )

        return summary

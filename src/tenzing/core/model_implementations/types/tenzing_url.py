import os
from pathlib import Path
from urllib.parse import urlparse, ParseResult

import pandas.api.types as pdt

from tenzing.core import tenzing_model
from tenzing.core.mixins.option_mixin import optionMixin
from tenzing.utils import singleton


@singleton.singleton_object
class tenzing_url(optionMixin, tenzing_model):
    """**Path** implementation of :class:`tenzing.core.models.tenzing_model`.

    >>> from urllib.parse import urlparse
    >>> x = pd.Series([urlparse('http://www.cwi.nl:80/%7Eguido/Python.html'), urlparse('https://github.com/pandas-profiling/pandas-profiling')])
    >>> x in tenzing_url
    True
    """
    def contains_op(self, series):
        if not pdt.is_object_dtype(series):
            return False

        return series.apply(lambda x: isinstance(x, ParseResult)).all()

    def cast_op(self, series):
        return series.apply(urlparse)

    def summarization_op(self, series):
        # TODO: inherit from 'unique'
        summary = series.agg(['nunique']).to_dict()
        # TODO: inherit from common base?
        summary['n_records'] = series.shape[0]
        summary['frequencies'] = series.value_counts().to_dict()

        # TODO: value counts for url parts

        return summary

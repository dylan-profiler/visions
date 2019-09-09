import os
from pathlib import Path

import pandas.api.types as pdt

from tenzing.core import tenzing_model
from tenzing.core.mixins.option_mixin import optionMixin
from tenzing.utils import singleton


@singleton.singleton_object
class tenzing_path(optionMixin, tenzing_model):
    """**Path** implementation of :class:`tenzing.core.models.tenzing_model`.

    >>> x = pd.Series([Path('/home/user/file.txt'), Path('/home/user/test2.txt')])
    >>> x in tenzing_path
    True
    """
    def contains_op(self, series):
        if not pdt.is_object_dtype(series):
            return False

        # TODO: only absolute Paths
        return series.eq(series.apply(Path)).all()

    def cast_op(self, series):
        return series.apply(Path)

    def summarization_op(self, series):
        # TODO: inherit from 'unique'
        summary = series.agg(['nunique']).to_dict()
        # TODO: inherit from common base?
        summary['n_records'] = series.shape[0]
        summary['frequencies'] = series.value_counts().to_dict()

        summary["common_prefix"] = os.path.commonprefix(list(series)) or "No common prefix",
        return summary

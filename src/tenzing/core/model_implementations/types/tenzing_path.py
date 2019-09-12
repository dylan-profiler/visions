import os
from pathlib import Path

import pandas.api.types as pdt

from tenzing.core.mixins import optionMixin
from tenzing.core.model_implementations.types.tenzing_object import tenzing_object
from tenzing.core.reuse import unique_summary
from tenzing.utils import singleton


# @singleton.singleton_object
class tenzing_path(tenzing_object):
    """**Path** implementation of :class:`tenzing.core.models.tenzing_model`.

    >>> x = pd.Series([Path('/home/user/file.txt'), Path('/home/user/test2.txt')])
    >>> x in tenzing_path
    True
    """

    def contains_op(self, series):
        if not pdt.is_object_dtype(series):
            return False

        return (
            series.eq(series.apply(Path)).all()
            and series.apply(lambda p: p.is_absolute()).all()
        )

    def cast_op(self, series):
        return series.apply(Path)

    @unique_summary
    def summarization_op(self, series):
        summary = super().summarization_op(series)

        summary["common_prefix"] = (
            os.path.commonprefix(list(series)) or "No common prefix"
        )
        summary["stem_counts"] = series.map(lambda x: x.stem).value_counts().to_dict()
        summary["suffix_counts"] = (
            series.map(lambda x: x.suffix).value_counts().to_dict()
        )
        summary["name_counts"] = series.map(lambda x: x.name).value_counts().to_dict()
        summary["parent_counts"] = (
            series.map(lambda x: x.parent).value_counts().to_dict()
        )
        return summary

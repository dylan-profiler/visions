import os
from pathlib import Path, PureWindowsPath, PurePosixPath

import pandas.api.types as pdt

from tenzing.core.model_implementations.types.tenzing_object import tenzing_object
from tenzing.core.reuse import unique_summary


class tenzing_path(tenzing_object):
    """**Path** implementation of :class:`tenzing.core.models.tenzing_model`.

    >>> x = pd.Series([Path('/home/user/file.txt'), Path('/home/user/test2.txt')])
    >>> x in tenzing_path
    True
    """

    @classmethod
    def contains_op(cls, series):
        if not pdt.is_object_dtype(series):
            return False

        return series.apply(lambda x: isinstance(x, PureWindowsPath) and x.is_absolute()).all() or series.apply(lambda x: isinstance(x, PurePosixPath) and x.is_absolute()).all()

    @classmethod
    def cast_op(cls, series, operation=None):
        return series.apply(Path)

    @classmethod
    @unique_summary
    def summarization_op(cls, series):
        summary = super().summarization_op(series)

        summary["common_prefix"] = (
            os.path.commonprefix(list(series)) or "No common prefix"
        )
        # On add drive, root, anchor?
        summary["stem_counts"] = series.map(lambda x: x.stem).value_counts().to_dict()
        summary["suffix_counts"] = (
            series.map(lambda x: x.suffix).value_counts().to_dict()
        )
        summary["name_counts"] = series.map(lambda x: x.name).value_counts().to_dict()
        summary["parent_counts"] = (
            series.map(lambda x: x.parent).value_counts().to_dict()
        )
        return summary

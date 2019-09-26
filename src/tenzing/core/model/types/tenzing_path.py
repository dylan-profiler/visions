from pathlib import Path, PureWindowsPath, PurePosixPath, PurePath

import pandas as pd

from tenzing.core.models import tenzing_model


class tenzing_path(tenzing_model):
    """**Path** implementation of :class:`tenzing.core.models.tenzing_model`.
    >>> x = pd.Series([Path('/home/user/file.txt'), Path('/home/user/test2.txt')])
    >>> x in tenzing_path
    True
    """

    @classmethod
    def contains_op(cls, series: pd.Series) -> bool:
        return series.apply(lambda x: isinstance(x, PurePath) and x.is_absolute()).all()

    @classmethod
    def cast_op(cls, series: pd.Series, operation=None) -> pd.Series:
        return series.apply(PurePath)

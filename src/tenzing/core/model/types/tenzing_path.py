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
        path_types = [PurePosixPath, PureWindowsPath]
        for path_type in path_types:
            is_path_type = series.apply(lambda x: isinstance(x, path_type)).all()
            if is_path_type:
                break

        if not is_path_type:
            return False
        elif series.apply(lambda x: x.is_absolute()).all():
            return True
        else:
            return False

    @classmethod
    def cast_op(cls, series: pd.Series, operation=None) -> pd.Series:
        return series.apply(PurePath)

from pathlib import Path, PureWindowsPath, PurePosixPath, PurePath

import pandas as pd

from tenzing.core.model.model_relation import relation_conf
from tenzing.core.model.models import tenzing_model


def string_is_path(series):
    try:
        s = to_path(series.copy())
        return s.apply(lambda x: x.is_absolute()).all()
    except TypeError:
        return False


def to_path(series: pd.Series) -> pd.Series:
    s = series.copy().apply(PureWindowsPath)
    if not s.apply(lambda x: x.is_absolute()).all():
        return series.apply(PurePosixPath)
    else:
        return s


class tenzing_path(tenzing_model):
    """**Path** implementation of :class:`tenzing.core.models.tenzing_model`.
    >>> x = pd.Series([Path('/home/user/file.txt'), Path('/home/user/test2.txt')])
    >>> x in tenzing_path
    True
    """

    @classmethod
    def get_relations(cls):
        from tenzing.core.model.types import tenzing_object,tenzing_string

        relations = {
            tenzing_object: relation_conf(inferential=False),
            tenzing_string: relation_conf(inferential=True, relationship=string_is_path, transformer=to_path)
        }
        return relations

    @classmethod
    def contains_op(cls, series: pd.Series) -> bool:
        return series.apply(lambda x: isinstance(x, PurePath) and x.is_absolute()).all()

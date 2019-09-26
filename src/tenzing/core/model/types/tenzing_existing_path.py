from pathlib import Path
import pandas as pd

from tenzing.core.models import tenzing_model


class tenzing_existing_path(tenzing_model):
    """**Existing Path** implementation of :class:`tenzing.core.models.tenzing_model`.
    >>> x = pd.Series([Path('/home/user/file.txt'), Path('/home/user/test2.txt')])
    >>> x in tenzing_existing_path
    True
    """

    @classmethod
    def contains_op(cls, series: pd.Series) -> bool:
        return series.apply(lambda p: isinstance(p, Path) and p.exists()).all()

    @classmethod
    def cast_op(cls, series: pd.Series, operation=None) -> pd.Series:
        return series.apply(Path)

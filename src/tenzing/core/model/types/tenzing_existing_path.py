from pathlib import Path
import pandas as pd

from tenzing.core.model.types.tenzing_path import tenzing_path


class tenzing_existing_path(tenzing_path):
    """**Existing Path** implementation of :class:`tenzing.core.models.tenzing_model`.

    >>> x = pd.Series([Path('/home/user/file.txt'), Path('/home/user/test2.txt')])
    >>> x in tenzing_existing_path
    True
    """

    @classmethod
    def contains_op(cls, series: pd.Series) -> bool:
        if not super().contains_op(series):
            return False

        return series.apply(lambda p: p.exists()).all()

    @classmethod
    def cast_op(cls, series: pd.Series, operation=None) -> pd.Series:
        return super().cast_op(series)

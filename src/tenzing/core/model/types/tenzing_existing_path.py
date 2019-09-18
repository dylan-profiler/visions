from pathlib import Path
import pandas as pd

from tenzing.core.model.types.tenzing_path import tenzing_path


class tenzing_existing_path(tenzing_path):
    """**Existing Path** implementation of :class:`tenzing.core.models.tenzing_model`.

    Examples:
        >>> x = pd.Series([Path('/home/user/file.txt'), Path('/home/user/test2.txt')])
        >>> x in tenzing_existing_path
        True
    """

    @classmethod
    def mask(cls, series: pd.Series) -> pd.Series:
        super_mask = super().mask(series)
        return super_mask & series[super_mask].apply(
            lambda p: isinstance(p, Path) and p.exists()
        )

    @classmethod
    def cast_op(cls, series: pd.Series, operation=None) -> pd.Series:
        return super().cast_op(series)

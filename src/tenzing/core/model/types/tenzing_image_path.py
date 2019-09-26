from tenzing.utils.monkeypatches import *
import imghdr
from pathlib import Path

import pandas as pd

from tenzing.core.models import tenzing_model


def path_is_image(p: Path):
    return imghdr.what(p) is not None


class tenzing_image_path(tenzing_model):
    """**Image Path** implementation of :class:`tenzing.core.models.tenzing_model`.
    >>> x = pd.Series([Path('/home/user/file.png'), Path('/home/user/test2.jpg')])
    >>> x in tenzing_image_path
    True
    """

    @classmethod
    def contains_op(cls, series: pd.Series) -> bool:
        return series.apply(lambda p: path_is_image(p)).all()

    @classmethod
    def cast_op(cls, series: pd.Series, operation=None) -> pd.Series:
        return super().cast_op(series)

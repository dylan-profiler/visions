import pandas as pd

from tenzing.core.model.types.tenzing_existing_path import tenzing_existing_path
from tenzing.utils.images.image_utils import path_is_image


class tenzing_image_path(tenzing_existing_path):
    """**Image Path** implementation of :class:`tenzing.core.models.tenzing_model`.

    Examples:
        >>> x = pd.Series([Path('/home/user/file.png'), Path('/home/user/test2.jpg')])
        >>> x in tenzing_image_path
        True
    """

    @classmethod
    def mask(cls, series: pd.Series) -> pd.Series:
        super_mask = super().mask(series)
        return super_mask & series[super_mask].apply(lambda p: path_is_image(p))

    @classmethod
    def cast_op(cls, series: pd.Series, operation=None) -> pd.Series:
        return super().cast_op(series)

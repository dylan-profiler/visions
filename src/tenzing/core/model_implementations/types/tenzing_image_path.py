from tenzing.utils.monkeypatches import *
import imghdr

from tenzing.core.model_implementations.types.tenzing_existing_path import (
    tenzing_existing_path,
)


def path_is_image(p: Path):
    return imghdr.what(p) is not None


class tenzing_image_path(tenzing_existing_path):
    """**Path** implementation of :class:`tenzing.core.models.tenzing_model`.

    >>> x = pd.Series([Path('/home/user/file.png'), Path('/home/user/test2.jpg')])
    >>> x in tenzing_image_path
    True
    """

    @classmethod
    def contains_op(cls, series):
        if not super().contains_op(series):
            return False

        return series.apply(lambda p: path_is_image(p)).all()

    @classmethod
    def cast_op(cls, series, operation=None):
        return super().cast_op(series)

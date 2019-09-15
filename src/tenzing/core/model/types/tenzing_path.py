from pathlib import Path, PureWindowsPath, PurePosixPath

from tenzing.core.model.types.tenzing_object import tenzing_object


class tenzing_path(tenzing_object):
    """**Path** implementation of :class:`tenzing.core.models.tenzing_model`.

    >>> x = pd.Series([Path('/home/user/file.txt'), Path('/home/user/test2.txt')])
    >>> x in tenzing_path
    True
    """

    @classmethod
    def contains_op(cls, series):
        if not super().contains_op(series):
            return False

        return (
            series.apply(
                lambda x: isinstance(x, PureWindowsPath) and x.is_absolute()
            ).all()
            or series.apply(
                lambda x: isinstance(x, PurePosixPath) and x.is_absolute()
            ).all()
        )

    @classmethod
    def cast_op(cls, series, operation=None):
        return series.apply(Path)

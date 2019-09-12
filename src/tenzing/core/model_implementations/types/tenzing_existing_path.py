from pathlib import Path

from tenzing.core.model_implementations.types.tenzing_path import tenzing_path


class tenzing_existing_path(tenzing_path):
    """**Path** implementation of :class:`tenzing.core.models.tenzing_model`.

    >>> x = pd.Series([Path('/home/user/file.txt'), Path('/home/user/test2.txt')])
    >>> x in tenzing_existing_path
    True
    """

    @classmethod
    def contains_op(cls, series):
        if not super().contains_op(series):
            return False

        return series.apply(lambda p: p.exists()).all()

    @classmethod
    def cast_op(cls, series, operation=None):
        return super().cast_op(series)

    @classmethod
    def summarization_op(cls, series):
        summary = super().summarization_op(series)
        summary["file_sizes"] = series.map(lambda x: x.stat().st_size)
        return summary

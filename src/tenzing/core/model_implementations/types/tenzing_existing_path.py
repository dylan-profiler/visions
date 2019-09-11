from pathlib import Path

from tenzing.core.model_implementations.types.tenzing_path import tenzing_path
from tenzing.utils import singleton


# @singleton.singleton_object
class tenzing_existing_path(tenzing_path):
    """**Path** implementation of :class:`tenzing.core.models.tenzing_model`.

    >>> x = pd.Series([Path('/home/user/file.txt'), Path('/home/user/test2.txt')])
    >>> x in tenzing_existing_path
    True
    """
    def contains_op(self, series):
        if not super().contains_op(series):
            return False

        return series.apply(lambda p: p.exists()).all()

    def cast_op(self, series):
        return super().cast_op(series)

    def summarization_op(self, series):
        summary = super().summarization_op(series)
        summary['file_sizes'] = series.map(lambda x: x.stat().st_size)
        return summary

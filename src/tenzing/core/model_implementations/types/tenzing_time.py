import pandas as pd

from tenzing.core.model_implementations.types.tenzing_datetime import tenzing_datetime


class tenzing_time(tenzing_datetime):
    """**Time** implementation of :class:`tenzing.core.models.tenzing_model`.

    >>> x = pd.Series([pd.datetime(2017, 3, 5), pd.datetime(2019, 12, 4)])
    >>> x in tenzing_time
    True
    """

    @classmethod
    def contains_op(cls, series):
        if not super().contains_op(series):
            return False

        return series.eq(
            series.copy().apply(lambda x: x.replace(day=1, month=1, year=1970))
        ).all()

    @classmethod
    def cast_op(cls, series, operation=None):
        return pd.to_datetime(series)

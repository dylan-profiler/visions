import pandas as pd

from tenzing.core.model.types.tenzing_datetime import tenzing_datetime


class tenzing_time(tenzing_datetime):
    """**Time** implementation of :class:`tenzing.core.models.tenzing_model`.

    Examples:
        >>> x = pd.Series([pd.datetime(2017, 3, 5), pd.datetime(2019, 12, 4)])
        >>> x in tenzing_time
        True
    """

    @classmethod
    def mask(cls, series: pd.Series) -> pd.Series:
        return series.eq(
            series.copy().apply(lambda x: x.replace(day=1, month=1, year=1970))
        )

    @classmethod
    def cast_op(cls, series: pd.Series, operation=None) -> pd.Series:
        return pd.to_datetime(series)

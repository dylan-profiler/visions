import pandas as pd

from tenzing.core.model.types.tenzing_datetime import tenzing_datetime


class tenzing_date(tenzing_datetime):
    """**Date** implementation of :class:`tenzing.core.models.tenzing_model`.

    Examples:
        >>> x = pd.Series([pd.datetime(2017, 3, 5), pd.datetime(2019, 12, 4)])
        >>> x in tenzing_date
        True
    """

    @classmethod
    def contains_op(cls, series: pd.Series) -> bool:
        if not super().contains_op(series):
            return False
        # TODO: https://stackoverflow.com/a/51529633/470433
        return series.eq(
            series.copy().apply(lambda x: x.replace(hour=0, minute=0, second=0))
        ).all()

    @classmethod
    def cast_op(cls, series: pd.Series, operation=None) -> pd.Series:
        return pd.to_datetime(series)

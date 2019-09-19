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
    def mask(cls, series: pd.Series) -> pd.Series:
        super_mask = super().mask(series)
        # TODO: https://stackoverflow.com/a/51529633/470433
        if not super_mask.any():
            return super_mask

        return super_mask & series[super_mask].eq(
            series[super_mask]
            .copy()
            .apply(lambda x: x.replace(hour=0, minute=0, second=0))
        )

    @classmethod
    def cast_op(cls, series: pd.Series, operation=None) -> pd.Series:
        return pd.to_datetime(series)

import pandas as pd
import pandas.api.types as pdt

from tenzing.core.model.models import tenzing_model


class tenzing_date(tenzing_model):
    """**Date** implementation of :class:`tenzing.core.models.tenzing_model`.
    >>> x = pd.Series([pd.datetime(2017, 3, 5), pd.datetime(2019, 12, 4)])
    >>> x in tenzing_date
    True
    """

    @classmethod
    def contains_op(cls, series: pd.Series) -> bool:
        return pdt.is_datetime64_any_dtype(series) and all(
            (
                series.dt.hour.eq(0).all(),
                series.dt.minute.eq(0).all(),
                series.dt.second.eq(0).all(),
            )
        )

    @classmethod
    def cast_op(cls, series: pd.Series, operation=None) -> pd.Series:
        return pd.to_datetime(series)

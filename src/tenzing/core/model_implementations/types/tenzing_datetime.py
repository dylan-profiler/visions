import pandas.api.types as pdt
import pandas as pd

from tenzing.core.model_implementations.types.tenzing_generic import tenzing_generic


class tenzing_datetime(tenzing_generic):
    """**Datetime** implementation of :class:`tenzing.core.models.tenzing_model`.

    >>> x = pd.Series([pd.datetime(2017, 3, 5), pd.datetime(2019, 12, 4)])
    >>> x in tenzing_datetime
    True
    """

    @classmethod
    def contains_op(cls, series):
        return (
            not series.empty
            and pdt.is_datetime64_any_dtype(series)
            and not series.hasnans
        )

    @classmethod
    def cast_op(cls, series, operation=None):
        return pd.to_datetime(series)

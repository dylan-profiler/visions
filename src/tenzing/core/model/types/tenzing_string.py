import pandas as pd

from tenzing.core.models import tenzing_model


class tenzing_string(tenzing_model):
    """**String** implementation of :class:`tenzing.core.models.tenzing_model`.
    >>> x = pd.Series(['rubin', 'carter', 'champion'])
    >>> x in tenzing_string
    True
    """

    @classmethod
    def contains_op(cls, series: pd.Series) -> bool:
        return series.map(type).eq(str).all()

    @classmethod
    def cast_op(cls, series: pd.Series, operation=None) -> pd.Series:
        return series.astype(str)

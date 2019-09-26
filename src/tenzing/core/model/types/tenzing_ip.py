import pandas as pd
from ipaddress import IPv4Address, _BaseAddress

from tenzing.core.models import tenzing_model


class tenzing_ip(tenzing_model):
    """**IP Address** implementation of :class:`tenzing.core.models.tenzing_model`.
    >>> x = pd.Series([IPv4Address('127.0.0.1'), IPv4Address('128.0.1.2')])
    >>> x in tenzing_ip
    True
    """

    @classmethod
    def contains_op(cls, series: pd.Series) -> bool:
        return series.apply(lambda x: isinstance(x, _BaseAddress)).all()

    @classmethod
    def cast_op(cls, series: pd.Series, operation=None) -> pd.Series:
        return series.apply(IPv4Address)

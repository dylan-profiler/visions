import pandas as pd
from ipaddress import IPv4Address, _BaseAddress, ip_address

from tenzing.core.model.types.tenzing_object import tenzing_object


class tenzing_ip(tenzing_object):
    """**IP Address** implementation of :class:`tenzing.core.models.tenzing_model`.

    Examples:
        >>> x = pd.Series([IPv4Address('127.0.0.1'), IPv4Address('184.168.42.1')])
        >>> x in tenzing_ip
        True
    """

    @classmethod
    def contains_op(cls, series: pd.Series) -> bool:
        if not super().contains_op(series):
            return False

        return series.apply(lambda x: isinstance(x, _BaseAddress)).all()

    @classmethod
    def cast_op(cls, series: pd.Series, operation=None) -> pd.Series:
        return series.apply(lambda x: ip_address(x))

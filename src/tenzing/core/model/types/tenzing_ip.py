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
    def mask(cls, series: pd.Series) -> pd.Series:
        super_mask = super().mask(series)
        if not super_mask.any():
            return super_mask

        return super_mask & series[super_mask].apply(lambda x: isinstance(x, _BaseAddress))

    @classmethod
    def cast_op(cls, series: pd.Series, operation=None) -> pd.Series:
        return series.apply(lambda x: ip_address(x))

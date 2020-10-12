from ipaddress import _BaseAddress, ip_address

import pandas as pd

from visions.backends.pandas_ import test_utils
from visions.backends.pandas_.series_utils import (
    series_handle_nulls,
    series_not_empty,
)
from visions.types.ip_address import IPAddress
from visions.types.string import String


@IPAddress.register_relationship(String, pd.Series)
def string_is_ip_address(series: pd.Series, state: dict) -> bool:
    return test_utils.coercion_test(lambda s: s.apply(ip_address))(series)


@IPAddress.register_transformer(String, pd.Series)
def string_to_ip_address(series: pd.Series, state: dict) -> pd.Series:
    return series.apply(ip_address)


@IPAddress.contains_op.register
@series_not_empty
@series_handle_nulls
def ip_address_contains(series: pd.Series, state: dict) -> bool:
    return all(isinstance(x, _BaseAddress) for x in series)

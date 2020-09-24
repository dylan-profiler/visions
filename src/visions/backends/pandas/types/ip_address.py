from ipaddress import _BaseAddress, ip_address

import pandas as pd

from visions.backends.pandas import test_utils
from visions.backends.pandas.series_utils import series_handle_nulls, series_not_empty
from visions.types.ip_address import (
    ip_address_contains,
    string_is_ip_address,
    string_to_ip_address,
)


@string_is_ip_address.register(pd.Series)
def _(series: pd.Series, state: dict) -> bool:
    return test_utils.coercion_test(lambda s: s.apply(ip_address))(series)


@string_to_ip_address.register(pd.Series)
def _(series: pd.Series, state: dict) -> pd.Series:
    return series.apply(ip_address)


@ip_address_contains.register(pd.Series)
@series_not_empty
@series_handle_nulls
def _(series: pd.Series, state: dict) -> bool:
    return all(isinstance(x, _BaseAddress) for x in series)

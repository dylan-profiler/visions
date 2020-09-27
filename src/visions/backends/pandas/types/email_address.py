import pandas as pd

from visions.backends.pandas import test_utils
from visions.backends.pandas.series_utils import (
    isinstance_attrs,
    series_handle_nulls,
    series_not_empty,
)
from visions.types.email_address import (
    FQDA,
    _to_email,
    email_address_contains,
    string_is_email,
    string_to_email,
)


@string_is_email.register(pd.Series)
def _(series: pd.Series, state: dict) -> bool:
    def test_email(s):
        return s.apply(_to_email).apply(lambda x: x.local and x.fqdn)

    return test_utils.coercion_true_test(test_email)(series)


@string_to_email.register(pd.Series)
def _(series: pd.Series, state: dict) -> pd.Series:
    return series.apply(_to_email)


@email_address_contains.register(pd.Series)
@series_not_empty
@series_handle_nulls
def _(series: pd.Series, state: dict) -> bool:
    return isinstance_attrs(series, FQDA, ["local", "fqdn"])

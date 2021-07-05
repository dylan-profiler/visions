import pandas as pd

from visions.backends.pandas import test_utils
from visions.backends.pandas.series_utils import (
    isinstance_attrs,
    series_handle_nulls,
    series_not_empty,
)
from visions.backends.shared.parallelization_engines import pandas_apply
from visions.types.email_address import FQDA, EmailAddress, _to_email
from visions.types.string import String


@EmailAddress.register_relationship(String, pd.Series)
def string_is_email(series: pd.Series, state: dict) -> bool:
    def test_email(s):
        return pandas_apply(pandas_apply(s, _to_email), lambda x: x.local and x.fqdn)

    return test_utils.coercion_true_test(test_email)(series)


@EmailAddress.register_transformer(String, pd.Series)
def string_to_email(series: pd.Series, state: dict) -> pd.Series:
    return pandas_apply(series, _to_email)


@EmailAddress.contains_op.register
@series_not_empty
@series_handle_nulls
def email_address_contains(series: pd.Series, state: dict) -> bool:
    return isinstance_attrs(series, FQDA, ["local", "fqdn"])

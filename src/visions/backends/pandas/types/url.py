from urllib.parse import ParseResult, urlparse

import pandas as pd

from visions.backends.pandas.series_utils import (
    isinstance_attrs,
    series_handle_nulls,
    series_not_empty,
)
from visions.backends.shared.parallelization_engines import pandas_apply
from visions.types.string import String
from visions.types.url import URL


@URL.register_relationship(String, pd.Series)
@series_handle_nulls
def string_is_url(series: pd.Series, state: dict) -> bool:
    try:
        return pandas_apply(
            string_to_url(series, state), lambda x: x.netloc and x.scheme
        ).all()
    except AttributeError:
        return False


@URL.register_transformer(String, pd.Series)
def string_to_url(series: pd.Series, state: dict) -> pd.Series:
    return pandas_apply(series, urlparse)


@URL.contains_op.register
@series_handle_nulls
@series_not_empty
def url_contains(series: pd.Series, state: dict) -> bool:
    return isinstance_attrs(series, ParseResult, ["netloc", "scheme"])

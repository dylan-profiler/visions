from urllib.parse import ParseResult, urlparse

import pandas as pd

from visions.backends.pandas.series_utils import (
    isinstance_attrs,
    series_handle_nulls,
    series_not_empty,
)
from visions.types.url import string_is_url, string_to_url, url_contains


@string_is_url.register(pd.Series)
@series_handle_nulls
def _(series: pd.Series, state: dict) -> bool:
    try:
        return string_to_url(series, state).apply(lambda x: x.netloc and x.scheme).all()
    except AttributeError:
        return False


@string_to_url.register(pd.Series)
def _(series: pd.Series, state: dict) -> pd.Series:
    return series.apply(urlparse)


@url_contains.register(pd.Series)
@series_handle_nulls
@series_not_empty
def _(series: pd.Series, state: dict) -> bool:
    return isinstance_attrs(series, ParseResult, ["netloc", "scheme"])

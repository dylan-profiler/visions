import uuid

import pandas as pd

from visions.backends.pandas.series_utils import (
    isinstance_attrs,
    series_handle_nulls,
    series_not_empty,
)
from visions.backends.pandas.test_utils import coercion_true_test
from visions.types.uuid import string_is_uuid, string_to_uuid, uuid_contains


@string_is_uuid.register(pd.Series)
def _(series: pd.Series, state: dict) -> bool:
    def f(s):
        return s.apply(uuid.UUID)

    return coercion_true_test(f)(series)


@string_to_uuid.register(pd.Series)
def _(series: pd.Series, state: dict) -> pd.Series:
    return series.apply(uuid.UUID)


@uuid_contains.register(pd.Series)
@series_not_empty
@series_handle_nulls
def _(series: pd.Series, state: dict) -> bool:
    return isinstance_attrs(series, uuid.UUID, ["time_low", "hex"])

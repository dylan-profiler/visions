import uuid

import pandas as pd

from visions.backends.pandas.series_utils import (
    isinstance_attrs,
    series_handle_nulls,
    series_not_empty,
)
from visions.backends.pandas.test_utils import coercion_true_test
from visions.backends.shared.parallelization_engines import pandas_apply
from visions.types.string import String
from visions.types.uuid import UUID


@UUID.register_relationship(String, pd.Series)
def uuid_is_string(series: pd.Series, state: dict) -> bool:
    def f(s):
        return pandas_apply(s, uuid.UUID)

    return coercion_true_test(f)(series)


@UUID.register_transformer(String, pd.Series)
def uuid_to_string(series: pd.Series, state: dict) -> pd.Series:
    return pandas_apply(series, uuid.UUID)


@UUID.contains_op.register
@series_not_empty
@series_handle_nulls
def uuid_contains(series: pd.Series, state: dict) -> bool:
    return isinstance_attrs(series, uuid.UUID, ["time_low", "hex"])

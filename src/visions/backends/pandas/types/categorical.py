import pandas as pd

from visions.backends.pandas.series_utils import (
    pandas_is_categorical,
    series_not_empty,
    series_not_sparse,
)
from visions.types.categorical import Categorical


@Categorical.contains_op.register
@series_not_sparse
@series_not_empty
def categorical_contains(series: pd.Series, state: dict) -> bool:
    return pandas_is_categorical(series)

import pandas as pd
from pandas.api import types as pdt

from visions.backends.pandas.series_utils import series_not_empty, series_not_sparse
from visions.types.categorical import categorical_contains


@categorical_contains.register(pd.Series)
@series_not_sparse
@series_not_empty
def _(series: pd.Series, state: dict) -> bool:
    return pdt.is_categorical_dtype(series)

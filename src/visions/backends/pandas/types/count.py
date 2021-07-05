import pandas as pd
from pandas.api import types as pdt

from visions.backends.pandas.series_utils import series_not_empty, series_not_sparse
from visions.types.count import Count


@Count.contains_op.register
@series_not_sparse
@series_not_empty
def count_contains(series: pd.Series, state: dict) -> bool:
    return pdt.is_unsigned_integer_dtype(series)

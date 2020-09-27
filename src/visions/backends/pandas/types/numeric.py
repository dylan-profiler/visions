import pandas as pd
from pandas.api import types as pdt

from visions.backends.pandas.series_utils import series_not_empty, series_not_sparse
from visions.types.numeric import numeric_contains_op


@numeric_contains_op.register(pd.Series)
@series_not_sparse
@series_not_empty
def _(series: pd.Series, state: dict) -> bool:
    return pdt.is_numeric_dtype(series)

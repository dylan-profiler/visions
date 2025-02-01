import pandas as pd
from pandas.api import types as pdt

from visions.backends.pandas.series_utils import series_not_empty, series_not_sparse
from visions.types.numeric import Numeric


@Numeric.contains_op.register
@series_not_sparse
@series_not_empty
def numeric_contains_op(series: pd.Series, state: dict) -> bool:
    return pdt.is_numeric_dtype(series)

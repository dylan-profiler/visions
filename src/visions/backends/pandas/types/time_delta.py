import pandas as pd
from pandas.api import types as pdt

from visions.backends.pandas.series_utils import series_not_empty, series_not_sparse
from visions.types.time_delta import TimeDelta


@TimeDelta.contains_op.register
@series_not_sparse
@series_not_empty
def time_delta_contains(series: pd.Series, state: dict) -> bool:
    """
    Example:
        >>> x = pd.Series([pd.Timedelta(days=i) for i in range(3)])
        >>> x in visions.Timedelta
        True
    """
    return pdt.is_timedelta64_dtype(series)

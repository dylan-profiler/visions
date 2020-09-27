import pandas as pd
from pandas.api import types as pdt

from visions.types.sparse import sparse_contains


@sparse_contains.register(pd.Series)
def _(series: pd.Series, state: dict) -> bool:
    return pdt.is_sparse(series)

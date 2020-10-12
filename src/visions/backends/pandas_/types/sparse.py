import pandas as pd
from pandas.api import types as pdt

from visions.types.sparse import Sparse


@Sparse.contains_op.register
def sparse_contains(series: pd.Series, state: dict) -> bool:
    return pdt.is_sparse(series)

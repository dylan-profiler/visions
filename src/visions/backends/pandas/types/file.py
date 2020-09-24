import pathlib

import pandas as pd

from visions.backends.pandas.series_utils import series_handle_nulls, series_not_empty
from visions.types.file import file_contains


@file_contains.register(pd.Series)
@series_not_empty
@series_handle_nulls
def _(series: pd.Series, state: dict) -> bool:
    return all(isinstance(p, pathlib.Path) and p.exists() for p in series)

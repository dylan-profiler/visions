import pathlib

import pandas as pd

from visions.backends.pandas.series_utils import series_handle_nulls, series_not_empty
from visions.types.file import File


@File.contains_op.register
@series_not_empty
@series_handle_nulls
def file_contains(series: pd.Series, state: dict) -> bool:
    return all(isinstance(p, pathlib.Path) and p.exists() for p in series)

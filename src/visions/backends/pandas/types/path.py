import pathlib

import pandas as pd

from visions.backends.pandas.series_utils import series_handle_nulls, series_not_empty
from visions.types.path import path_contains, string_is_path, string_to_path


@path_contains.register(pd.Series)
@series_not_empty
@series_handle_nulls
def contains_op(series: pd.Series, state: dict) -> bool:
    return all(isinstance(x, pathlib.PurePath) and x.is_absolute() for x in series)


@string_is_path.register(pd.Series)
def _(series: pd.Series, state: dict) -> bool:
    try:
        s = string_to_path(series.copy(), state)
        return s.apply(lambda x: x.is_absolute()).all()
    except TypeError:
        return False


@string_to_path.register(pd.Series)
def _(series: pd.Series, state: dict) -> pd.Series:
    s = series.copy().apply(pathlib.PureWindowsPath)
    if not s.apply(lambda x: x.is_absolute()).all():
        return series.apply(pathlib.PurePosixPath)
    else:
        return s

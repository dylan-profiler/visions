import pathlib

import pandas as pd

from visions.backends.pandas_be.series_utils import (
    series_handle_nulls,
    series_not_empty,
)
from visions.types.path import Path
from visions.types.string import String


@Path.register_relationship(String, pd.Series)
def string_is_path(series: pd.Series, state: dict) -> bool:
    try:
        s = string_to_path(series.copy(), state)
        return s.apply(lambda x: x.is_absolute()).all()
    except TypeError:
        return False


@Path.register_transformer(String, pd.Series)
def string_to_path(series: pd.Series, state: dict) -> pd.Series:
    s = series.copy().apply(pathlib.PureWindowsPath)
    if not s.apply(lambda x: x.is_absolute()).all():
        return series.apply(pathlib.PurePosixPath)
    else:
        return s


@Path.contains_op.register
@series_not_empty
@series_handle_nulls
def path_contains(series: pd.Series, state: dict) -> bool:
    return all(isinstance(x, pathlib.PurePath) and x.is_absolute() for x in series)

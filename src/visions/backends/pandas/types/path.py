import pathlib

import pandas as pd

from visions.backends.pandas.parallelization_engines import pandas_apply
from visions.backends.pandas.series_utils import series_handle_nulls, series_not_empty
from visions.types.path import Path
from visions.types.string import String


@Path.register_relationship(String, pd.Series)
def string_is_path(series: pd.Series, state: dict) -> bool:
    try:
        s = string_to_path(series.copy(), state)
        return pandas_apply(s, lambda x: x.is_absolute()).all()
    except TypeError:
        return False


@Path.register_transformer(String, pd.Series)
def string_to_path(series: pd.Series, state: dict) -> pd.Series:
    s = pandas_apply(series, pathlib.PureWindowsPath)
    if not pandas_apply(s, lambda x: x.is_absolute()).all():
        return pandas_apply(series, pathlib.PurePosixPath)
    else:
        return s


@Path.contains_op.register
@series_not_empty
@series_handle_nulls
def path_contains(series: pd.Series, state: dict) -> bool:
    return all(isinstance(x, pathlib.PurePath) and x.is_absolute() for x in series)

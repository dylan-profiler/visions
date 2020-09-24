import pandas as pd

from visions.backends.pandas.series_utils import series_handle_nulls, series_not_empty
from visions.types.geometry import geometry_contains, string_to_geometry


@string_to_geometry.register(pd.Series)
def _(series: pd.Series, state: dict) -> pd.Series:
    from shapely import wkt

    return pd.Series([wkt.loads(value) for value in series])


@geometry_contains.register(pd.Series)
@series_not_empty
@series_handle_nulls
def _(series: pd.Series, state: dict) -> bool:
    from shapely.geometry.base import BaseGeometry

    return all(issubclass(type(x), BaseGeometry) for x in series)

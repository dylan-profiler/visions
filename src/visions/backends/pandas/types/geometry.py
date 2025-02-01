import os
import sys

import pandas as pd

from visions.backends.pandas.series_utils import series_handle_nulls, series_not_empty
from visions.types.geometry import Geometry
from visions.types.string import String


# TODO: Evaluate https://jorisvandenbossche.github.io/blog/2019/08/13/geopandas-extension-array-refactor/
@Geometry.register_relationship(String, pd.Series)
def string_is_geometry(sequence: pd.Series, state: dict) -> bool:
    """Shapely logs failures at a silly severity, just trying to suppress it's output on failures."""
    from shapely import wkt
    from shapely.errors import WKTReadingError

    # only way to get rid of sys output when wkt.loads hits a bad value
    # TODO: use coercion wrapper for this
    sys.stderr = open(os.devnull, "w")
    try:
        result = all(wkt.loads(value) for value in sequence)
    except (
        WKTReadingError,
        AttributeError,
        UnicodeEncodeError,
        TypeError,
        UnicodeDecodeError,
    ):
        result = False
    finally:
        sys.stderr = sys.__stderr__
    return result


@Geometry.register_transformer(String, pd.Series)
def string_to_geometry(series: pd.Series, state: dict) -> pd.Series:
    from shapely import wkt

    return pd.Series([wkt.loads(value) for value in series])


@Geometry.contains_op.register
@series_not_empty
@series_handle_nulls
def geometry_contains(series: pd.Series, state: dict) -> bool:
    from shapely.geometry.base import BaseGeometry

    return all(issubclass(type(x), BaseGeometry) for x in series)

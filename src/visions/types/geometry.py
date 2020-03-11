import sys
import os
from typing import Sequence

import pandas as pd

from visions.relations import IdentityRelation, InferenceRelation, TypeRelation
from visions.types import VisionsBaseType


def string_is_geometry(series: pd.Series) -> bool:
    """Shapely logs failures at a silly severity, just trying to suppress it's output on failures."""
    from shapely import wkt
    from shapely.errors import WKTReadingError

    # only way to get rid of sys output when wkt.loads hits a bad value
    sys.stderr = open(os.devnull, "w")
    try:
        result = all(wkt.loads(value) for value in series)
    except (WKTReadingError, AttributeError, UnicodeEncodeError):
        result = False
    finally:
        sys.stderr = sys.__stderr__
    return result


def to_geometry(series: pd.Series) -> pd.Series:
    from shapely import wkt

    return pd.Series([wkt.loads(value) for value in series])


def _get_relations(cls) -> Sequence[TypeRelation]:
    from visions.types import String, Object

    relations = [
        IdentityRelation(cls, Object),
        InferenceRelation(
            cls, String, relationship=string_is_geometry, transformer=to_geometry
        ),
    ]
    return relations


# https://jorisvandenbossche.github.io/blog/2019/08/13/geopandas-extension-array-refactor/
class Geometry(VisionsBaseType):
    """**Geometry** implementation of :class:`visions.types.type.VisionsBaseType`.

    Examples:
        >>> from shapely import wkt
        >>> x = pd.Series([wkt.loads('POINT (-92 42)'), wkt.loads('POINT (-92 42.1)'), wkt.loads('POINT (-92 42.2)')]
        >>> x in visions.geometry
        True
    """

    @classmethod
    def get_relations(cls) -> Sequence[TypeRelation]:
        return _get_relations(cls)

    @classmethod
    def contains_op(cls, series: pd.Series) -> bool:
        from shapely.geometry.base import BaseGeometry

        return all(issubclass(type(x), BaseGeometry) for x in series)

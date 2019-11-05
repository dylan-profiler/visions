import pandas as pd
import sys
import os
from visions.core.model.model_relation import relation_conf
from visions.core.model.type import VisionsBaseType


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


# https://jorisvandenbossche.github.io/blog/2019/08/13/geopandas-extension-array-refactor/
class visions_geometry(VisionsBaseType):
    """**Geometry** implementation of :class:`visions.core.model.type.VisionsBaseType`.

    Examples:
        >>> from shapely import wkt
        >>> x = pd.Series([wkt.loads('POINT (-92 42)'), wkt.loads('POINT (-92 42.1)'), wkt.loads('POINT (-92 42.2)')]
        >>> x in visions_geometry
        True
    """

    @classmethod
    def get_relations(cls):
        from visions.core.implementations.types import visions_string, visions_object

        relations = {
            visions_string: relation_conf(
                relationship=string_is_geometry,
                transformer=to_geometry,
                inferential=True,
            ),
            visions_object: relation_conf(inferential=False),
        }
        return relations

    @classmethod
    def contains_op(cls, series: pd.Series) -> bool:
        from shapely.geometry.base import BaseGeometry

        return all(issubclass(type(x), BaseGeometry) for x in series)

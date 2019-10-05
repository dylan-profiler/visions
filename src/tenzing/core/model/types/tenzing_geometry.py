import pandas as pd
import logging

from tenzing.core.model.model_relation import relation_conf
from tenzing.core.model.models import tenzing_model


def string_is_geometry(series):
    """Shapely logs failures at a silly severity, just trying to suppress it's output on failures."""
    from shapely import wkt
    from shapely.errors import WKTReadingError

    logging.disable(logging.ERROR)
    try:
        result = all(wkt.loads(value) for value in series)
    except (WKTReadingError, AttributeError):
        result = False
    finally:
        logging.disable(logging.NOTSET)
    return result


def to_geometry(series: pd.Series) -> pd.Series:
    from shapely import wkt

    return pd.Series([wkt.loads(value) for value in series])


# https://jorisvandenbossche.github.io/blog/2019/08/13/geopandas-extension-array-refactor/
class tenzing_geometry(tenzing_model):
    """**Geometry** implementation of :class:`tenzing.core.models.tenzing_model`.
    >>> from shapely import wkt
    >>> x = pd.Series([wkt.loads('POINT (-92 42)'), wkt.loads('POINT (-92 42.1)'), wkt.loads('POINT (-92 42.2)')]
    >>> x in tenzing_geometry
    True
    """

    @classmethod
    def get_relations(cls):
        from tenzing.core.model.types import tenzing_string, tenzing_object

        relations = {
            tenzing_string: relation_conf(relationship=string_is_geometry, transformer=to_geometry, inferential=True),
            tenzing_object: relation_conf(inferential=False),
        }
        return relations

    @classmethod
    def contains_op(cls, series: pd.Series) -> bool:
        from shapely.geometry.base import BaseGeometry

        return series.apply(lambda x: issubclass(type(x), BaseGeometry)).all()
        # The below raises `TypeError: data type "geometry" not understood`
        # return series.dtype == 'geometry'

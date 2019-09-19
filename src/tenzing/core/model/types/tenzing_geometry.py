import pandas as pd
from shapely.geometry.base import BaseGeometry
from shapely import wkt
from shapely import geometry

from tenzing.core.model.types.tenzing_object import tenzing_object


class tenzing_geometry(tenzing_object):
    """**Geometry** implementation of :class:`tenzing.core.models.tenzing_model`.

    Examples:
        >>> from shapely import wkt
        >>> x = pd.Series([wkt.loads('POINT (-92 42)'), wkt.loads('POINT (-92 42.1)'), wkt.loads('POINT (-92 42.2)')]
        >>> x in tenzing_geometry
        True
    """

    geom_types = [
        geometry.Point,
        geometry.Polygon,
        geometry.MultiPolygon,
        geometry.MultiPoint,
        geometry.LineString,
        geometry.LinearRing,
        geometry.MultiPoint,
        geometry.MultiLineString,
    ]

    @classmethod
    def mask(cls, series: pd.Series) -> pd.Series:
        super_mask = super().mask(series)

        if not super_mask.any():
            return super_mask

        return super_mask & series[super_mask].apply(
            lambda x: any(isinstance(x, geom_type) for geom_type in cls.geom_types)
        )

    @classmethod
    def cast_op(cls, series: pd.Series, operation=None) -> pd.Series:
        return pd.Series(
            [
                wkt.loads(value) if not issubclass(type(value), BaseGeometry) else value
                for value in series
            ]
        )

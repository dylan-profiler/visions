import pandas as pd

from tenzing.core.models import tenzing_model


class tenzing_geometry(tenzing_model):
    """**Geometry** implementation of :class:`tenzing.core.models.tenzing_model`.
    >>> from shapely import wkt
    >>> x = pd.Series([wkt.loads('POINT (-92 42)'), wkt.loads('POINT (-92 42.1)'), wkt.loads('POINT (-92 42.2)')]
    >>> x in tenzing_geometry
    True
    """

    from shapely import geometry

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
    def contains_op(cls, series: pd.Series) -> bool:
        return all(
            any(isinstance(obj, geom_type) for geom_type in cls.geom_types)
            for obj in series
        )

    @classmethod
    def cast_op(cls, series: pd.Series, operation=None) -> pd.Series:
        from shapely import wkt

        return pd.Series([wkt.loads(value) for value in series])

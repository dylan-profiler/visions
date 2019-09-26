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
    from shapely.geometry import BaseGeometry

    @classmethod
    def contains_op(cls, series: pd.Series) -> bool:
        return series.apply(lambda x: issubclass(type(x), BaseGeometry)).all()

    @classmethod
    def cast_op(cls, series: pd.Series, operation=None) -> pd.Series:
        from shapely import wkt

        return pd.Series([wkt.loads(value) for value in series])

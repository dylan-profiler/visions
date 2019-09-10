import pandas.api.types as pdt
import pandas as pd

from tenzing.core import tenzing_model
from tenzing.core.mixins import baseSummaryMixin
from tenzing.core.mixins.option_mixin import optionMixin
from tenzing.utils import singleton


@singleton.singleton_object
class tenzing_geometry(baseSummaryMixin, optionMixin, tenzing_model):
    """**Geometry** implementation of :class:`tenzing.core.models.tenzing_model`.

    >>> from shapely import wkt
    >>> x = pd.Series([wkt.loads('POINT (-92 42)'), wkt.loads('POINT (-92 42.1)'), wkt.loads('POINT (-92 42.2)')]
    >>> x in tenzing_geometry
    True
    """
    from shapely import geometry
    geom_types = [geometry.Point, geometry.Polygon, geometry.MultiPolygon, geometry.MultiPoint,
                  geometry.LineString, geometry.LinearRing, geometry.MultiPoint, geometry.MultiLineString]

    def contains_op(self, series):
        return all(any(isinstance(obj, geom_type) for geom_type in self.geom_types) for obj in series)

    def cast_op(self, series):
        from shapely import wkt
        return pd.Series([wkt.loads(value) for value in series])

    def summarization_op(self, series):
        summary = super().summarization_op(series)

        try:
            import geopandas as gpd
            # summary['image'] = plotting.save_plot_to_str(gpd.GeoSeries(series).plot())
        except ImportError:
            pass

        return summary
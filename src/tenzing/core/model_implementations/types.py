from tenzing.core.models import tenzing_model, model_relation
from tenzing.core.mixins import optionMixin
from tenzing.utils import singleton, test_utils
from tenzing.core import plotting
from tenzing.core.summary import create_frequency_table
import os
import logging
import pandas.api.types as pdt
import pandas as pd
import seaborn as sn


@singleton.singleton_object
class tenzing_integer(optionMixin, tenzing_model):
    """**Integer** implementation of :class:`tenzing.core.models.tenzing_model`.

    >>> x = pd.Series([1, 2, 3, np.nan])
    >>> x in tenzing_integer
    True
    """
    def contains_op(self, series):
        if pdt.is_integer_dtype(series):
            return True
        elif pdt.is_float_dtype(series):
            # Need this additional check because it's an Option[Int] which in
            # pandas land will result in integers with decimal trailing 0's
            return series.eq(series.astype(int)).all()
        else:
            return False

    def cast_op(self, series):
        return series.astype(int)

    def summarization_op(self, series):
        aggregates = ['nunique', 'mean', 'std', 'max', 'min', 'median']
        summary = series.agg(aggregates).to_dict()
        summary['n_records'] = series.shape[0]

        summary['n_zeros'] = (series == 0).sum()
        summary['perc_zeros'] = summary['n_zeros'] / summary['n_records']

        summary['image'] = plotting.histogram(series)
        return summary


@singleton.singleton_object
class tenzing_float(optionMixin, tenzing_model):
    """**Float** implementation of :class:`tenzing.core.models.tenzing_model`.

    >>> x = pd.Series([1.0, 2.5, 5.0, np.nan])
    >>> x in tenzing_float
    True
    """
    def contains_op(self, series):
        if not pdt.is_float_dtype(series):
            return False
        elif series in tenzing_integer:
            return False
        else:
            return True

    def cast_op(self, series):
        return series.astype(float)

    def summarization_op(self, series):
        aggregates = ['nunique', 'mean', 'std', 'max', 'min', 'median']
        summary = series.agg(aggregates).to_dict()
        summary['n_records'] = series.shape[0]

        summary['n_zeros'] = (series == 0).sum()
        summary['perc_zeros'] = summary['n_zeros'] / summary['n_records']
        summary['image'] = plotting.histogram(series)
        return summary


@singleton.singleton_object
class tenzing_bool(optionMixin, tenzing_model):
    """**Boolean** implementation of :class:`tenzing.core.models.tenzing_model`.

    >>> x = pd.Series([True, False, np.nan])
    >>> x in tenzing_bool
    True
    """
    def contains_op(self, series):
        if pdt.is_categorical_dtype(series):
            return False
        return pdt.is_bool_dtype(series)

    def cast_op(self, series):
        return series.astype(bool)

    def summarization_op(self, series):
        summary = {}
        summary['frequencies'] = series.value_counts().to_dict()
        summary['num_True'] = summary['frequencies'].get(True, 0)
        summary['num_False'] = summary['frequencies'].get(False, 0)

        summary['n_records'] = series.shape[0]

        summary['perc_True'] = summary['num_True'] / summary['n_records']
        summary['perc_False'] = summary['num_False'] / summary['n_records']
        return summary


@singleton.singleton_object
class tenzing_categorical(optionMixin, tenzing_model):
    """**Categorical** implementation of :class:`tenzing.core.models.tenzing_model`.

    >>> x = pd.Series([True, False, 1], dtype='category')
    >>> x in tenzing_categorical
    True
    """
    def contains_op(self, series):
        return pdt.is_categorical_dtype(series)

    def cast_op(self, series):
        return series.astype('category')

    def summarization_op(self, series):
        aggregates = ['nunique']
        summary = series.agg(aggregates).to_dict()

        summary['category_size'] = len(series.dtype._categories)
        summary['missing_categorical_values'] = True if summary['nunique'] != summary['category_size'] else False
        summary['frequencies'] = series.value_counts().to_dict()
        return summary


@singleton.singleton_object
class tenzing_complex(optionMixin, tenzing_model):
    """**Complex** implementation of :class:`tenzing.core.models.tenzing_model`.

    >>> x = pd.Series([np.complex(0, 0), np.complex(1, 2), np.complex(3, -1), np.nan])
    >>> x in tenzing_complex
    True
    """
    def contains_op(self, series):
        return pdt.is_complex_dtype(series)

    def cast_op(self, series):
        return series.astype('complex')

    def summarization_op(self, series):
        aggregates = ['mean']
        summary = series.agg(aggregates).to_dict()
        summary['nunique'] = len(set(series))  # nunique apparently only considers real
        return summary


@singleton.singleton_object
class tenzing_timestamp(optionMixin, tenzing_model):
    """**Timestamp** implementation of :class:`tenzing.core.models.tenzing_model`.

    >>> x = pd.Series([pd.datetime(2017, 3, 5), pd.datetime(2019, 12, 4)])
    >>> x in tenzing_timestamp
    True
    """
    def contains_op(self, series):
        return pdt.is_datetime64_dtype(series)

    def cast_op(self, series):
        return pd.to_datetime(series)

    def summarization_op(self, series):
        aggregates = ['nunique', 'min', 'max']
        summary = series.agg(aggregates).to_dict()

        summary['n_records'] = series.shape[0]
        summary['perc_unique'] = summary['nunique'] / summary['n_records']

        summary['range'] = summary['max'] - summary['min']
        summary['image'] = plotting.save_plot_to_str(series.hist())
        return summary


@singleton.singleton_object
class tenzing_object(optionMixin, tenzing_model):
    """**Object** implementation of :class:`tenzing.core.models.tenzing_model`.

    >>> x = pd.Series(['a', 1, np.nan])
    >>> x in tenzing_object
    True
    """
    def contains_op(self, series):
        return pdt.is_object_dtype(series)

    def cast_op(self, series):
        return series.astype('object'),

    def summarization_op(self, series):
        summary = {}
        try:
            summary['nunique'] = series.nunique()
            summary['frequencies'] = series.value_counts().to_dict()
        except Exception:
            pass

        summary['n_records'] = series.shape[0]
        return summary


@singleton.singleton_object
class tenzing_string(optionMixin, tenzing_model):
    """**String** implementation of :class:`tenzing.core.models.tenzing_model`.

    >>> x = pd.Series(['a', 'b', np.nan])
    >>> x in tenzing_string
    True
    """
    def contains_op(self, series):
        if not pdt.is_object_dtype(series):
            return False

        return series.eq(series.astype(str)).all()

    def cast_op(self, series):
        return series.astype(str)

    def summarization_op(self, series):
        summary = series.agg(['nunique']).to_dict()
        summary['n_records'] = series.shape[0]
        summary['frequencies'] = series.value_counts().to_dict()
        return summary


@singleton.singleton_object
class tenzing_geometry(optionMixin, tenzing_model):
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
        summary = {}
        try:
            import geopandas as gpd
            summary['image'] = plotting.save_plot_to_str(gpd.GeoSeries(series).plot())
        except ImportError:
            pass

        return summary


def register_integer_relations():
    relations = [
        model_relation(tenzing_integer, tenzing_float,
                       test_utils.coercion_equality_test(lambda s: s.astype(int))),
        model_relation(tenzing_integer, tenzing_string,
                       test_utils.coercion_test(lambda s: s.astype(int))),
    ]
    for relation in relations:
        tenzing_integer.register_relation(relation)


def register_float_relations():
    def test_string_is_float(series):
        coerced_series = test_utils.option_coercion_evaluator(tenzing_float.cast)(series)
        if coerced_series is None:
            return False
        else:
            return True
    relations = [
        model_relation(tenzing_float, tenzing_string, test_string_is_float),
    ]
    for relation in relations:
        tenzing_float.register_relation(relation)


def register_string_relations():
    relations = [
        model_relation(tenzing_string, tenzing_object),
    ]
    for relation in relations:
        tenzing_string.register_relation(relation)


def register_timestamp_relations():

    relations = [
        model_relation(tenzing_timestamp, tenzing_string,
                       test_utils.coercion_test(lambda s: pd.to_datetime(s))),
        model_relation(tenzing_timestamp, tenzing_object)
    ]
    for relation in relations:
        tenzing_timestamp.register_relation(relation)


def register_geometry_relations():
    def string_is_geometry(series):
        """
            Shapely logs failures at a silly severity, just trying to suppress it's output on failures.
        """
        from shapely import wkt
        logging.disable()
        try:
            result = all(wkt.loads(value) for value in series)
        except Exception:
            result = False
        finally:
            logging.disable(logging.NOTSET)

        return result

    relations = [
        model_relation(tenzing_geometry, tenzing_string, string_is_geometry),
        model_relation(tenzing_geometry, tenzing_object, transformer=lambda series: series)
    ]
    for relation in relations:
        tenzing_geometry.register_relation(relation)


class string_bool_relation:
    _boolean_maps = {'true': True, 'True': True,
                     'false': False, 'False': False,
                     'TRUE': True, 'FALSE': False}

    def string_is_bool(self, series):
        return series.isin(self._boolean_maps.keys()).all()

    def map_string_to_bool(self, series):
        return series.map(self._boolean_maps)


def register_bool_relations():
    sb_relation = string_bool_relation()
    relations = [
        model_relation(tenzing_bool, tenzing_string,
                       sb_relation.string_is_bool, sb_relation.map_string_to_bool)
    ]
    for relation in relations:
        tenzing_bool.register_relation(relation)


register_integer_relations()
register_float_relations()
register_string_relations()
register_timestamp_relations()
register_bool_relations()
register_geometry_relations()

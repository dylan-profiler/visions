from tenzing.core.models import tenzing_model, model_relation
from tenzing.core.mixins import optionMixin
from tenzing.utils import singleton
import pandas.api.types as pdt


@singleton.singleton_object
class tenzing_integer(optionMixin, tenzing_model):
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
        return summary


@singleton.singleton_object
class tenzing_float(optionMixin, tenzing_model):
    def contains_op(self, series):
        if not pdt.is_float_dtype(series):
            return False
        elif series in tenzing_integer:
            return False
        else:
            return True

    def cast_op(self, series):
        return series.as_type(float)

    def summarization_op(self, series):
        aggregates = ['nunique', 'mean', 'std', 'max', 'min', 'median']
        summary = series.agg(aggregates).to_dict()
        summary['n_records'] = series.shape[0]

        summary['n_zeros'] = (series == 0).sum()
        summary['perc_zeros'] = summary['n_zeros'] / summary['n_records']
        return summary


@singleton.singleton_object
class tenzing_bool(optionMixin, tenzing_model):
    def contains_op(self, series):
        if pdt.is_categorical_dtype(series):
            return False
        return pdt.is_bool_dtype(series)

    def cast_op(self, series):
        pass

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
        return summary


@singleton.singleton_object
class tenzing_object(optionMixin, tenzing_model):
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
    def contains_op(self, series):
        if not pdt.is_object_dtype(series):
            return False

        return series.eq(series.astype(str)).all()

    def cast_op(self, series):
        pass

    def summarization_op(self, series):
        summary = series.agg(['nunique']).to_dict()
        summary['n_records'] = series.shape[0]
        summary['frequencies'] = series.value_counts().to_dict()
        return summary


@singleton.singleton_object
class tenzing_geometry(optionMixin, tenzing_model):
    from shapely import geometry, wkt
    geom_types = [geometry.Point, geometry.Polygon, geometry.MultiPolygon, geometry.MultiPoint,
                  geometry.LineString, geometry.LinearRing, geometry.MultiPoint, geometry.MultiLineString]

    def contains_op(self, series):
        return all(any(isinstance(obj, geom_type) for geom_type in self.geom_types) for obj in series)

    def cast_op(self, series):
        return [wkt.loads(value) for value in series]

    def summarization_op(self, series):
        summary = {}
        return summary


def register_integer_relations():
    relations = [
        model_relation(tenzing_integer, tenzing_float),
    ]
    for relation in relations:
        tenzing_integer.register_relation(relation)


def register_string_relations():
    relations = [
        model_relation(tenzing_string, tenzing_object),
    ]
    for relation in relations:
        tenzing_string.register_relation(relation)


register_string_relations()
register_integer_relations()

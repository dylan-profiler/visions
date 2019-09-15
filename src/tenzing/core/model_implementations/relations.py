from pathlib import Path
from urllib.parse import urlparse

from tenzing.core.model_implementations.types import *
from tenzing.core.models import model_relation
from tenzing.utils import test_utils
import logging
import pandas as pd


def register_integer_relations():
    relations = [
        model_relation(tenzing_integer, tenzing_generic),
        model_relation(
            tenzing_integer,
            tenzing_float,
            test_utils.coercion_equality_test(lambda s: s.astype(int)),
        ),
        model_relation(
            tenzing_integer,
            tenzing_string,
            test_utils.coercion_test(lambda s: s.astype(int)),
        ),
    ]
    for relation in relations:
        tenzing_integer.register_relation(relation)


def register_float_relations():
    def test_string_is_float(series):
        coerced_series = test_utils.option_coercion_evaluator(tenzing_float.cast)(
            series
        )
        if coerced_series is None:
            return False
        else:
            return True

    relations = [
        model_relation(tenzing_float, tenzing_generic),
        model_relation(tenzing_float, tenzing_string, test_string_is_float),
    ]
    for relation in relations:
        tenzing_float.register_relation(relation)


def register_string_relations():
    relations = [model_relation(tenzing_string, tenzing_object)]
    for relation in relations:
        tenzing_string.register_relation(relation)


def register_url_relations():
    def test_url(series):
        try:
            return (
                series.apply(urlparse).apply(lambda x: all((x.netloc, x.scheme))).all()
            )
        except AttributeError:
            return False

    relations = [model_relation(tenzing_url, tenzing_string, test_url)]
    for relation in relations:
        tenzing_url.register_relation(relation)


def register_path_relations():
    relations = [
        model_relation(
            tenzing_path,
            tenzing_string,
            lambda s: s.apply(lambda x: Path(x).is_absolute()).all(),
        ),
        model_relation(tenzing_path, tenzing_object),
    ]
    for relation in relations:
        tenzing_path.register_relation(relation)


def register_datetime_relations():
    relations = [
        model_relation(
            tenzing_datetime,
            tenzing_string,
            test_utils.coercion_test(lambda s: pd.to_datetime(s)),
        ),
        model_relation(tenzing_datetime, tenzing_object),
    ]
    for relation in relations:
        tenzing_datetime.register_relation(relation)


def register_timedelta_relations():
    relations = [model_relation(tenzing_timedelta, tenzing_object)]
    for relation in relations:
        tenzing_timedelta.register_relation(relation)


def register_geometry_relations():
    def string_is_geometry(series):
        """
            Shapely logs failures at a silly severity, just trying to suppress it's output on failures.
        """
        from shapely import wkt

        logging.disable(logging.ERROR)
        try:
            result = all(wkt.loads(value) for value in series)
        except Exception:
            result = False
        finally:
            logging.disable(logging.NOTSET)
        return result

    relations = [
        model_relation(tenzing_geometry, tenzing_string, string_is_geometry),
        model_relation(
            tenzing_geometry, tenzing_object, transformer=lambda series: series
        ),
    ]
    for relation in relations:
        tenzing_geometry.register_relation(relation)


def register_bool_relations():
    class string_bool_relation:
        _boolean_maps = [
            {"true": True, "false": False},
            {"y": True, "n": False},
            {"yes": True, "no": False},
        ]

        def __init__(self):
            self._full_boolean_map = {
                k: v for d in self._boolean_maps for k, v in d.items()
            }

        # TODO: ensure that series.str.lower() has no side effects
        def string_is_bool(self, series):
            temp_series = series.str.lower()
            return any(
                temp_series.isin(boolean_map.keys()).all()
                for boolean_map in self._boolean_maps
            )

        def map_string_to_bool(self, series):
            return series.str.lower().map(self._full_boolean_map)

    sb_relation = string_bool_relation()
    relations = [
        model_relation(tenzing_bool, tenzing_generic),
        model_relation(
            tenzing_bool,
            tenzing_string,
            sb_relation.string_is_bool,
            sb_relation.map_string_to_bool,
        ),
    ]
    for relation in relations:
        tenzing_bool.register_relation(relation)


def register_categorical_relations():
    register_type = tenzing_categorical
    relations = [model_relation(register_type, tenzing_generic)]
    for relation in relations:
        register_type.register_relation(relation)


def register_complex_relations():
    relations = [model_relation(tenzing_complex, tenzing_generic)]
    for relation in relations:
        tenzing_complex.register_relation(relation)


def register_object_relations():
    relations = [model_relation(tenzing_object, tenzing_generic)]
    for relation in relations:
        tenzing_object.register_relation(relation)


def register_date_relations():
    relations = [model_relation(tenzing_date, tenzing_datetime)]
    for relation in relations:
        tenzing_date.register_relation(relation)


def register_time_relations():
    relations = [model_relation(tenzing_time, tenzing_datetime)]
    for relation in relations:
        tenzing_time.register_relation(relation)


def register_existing_path_relations():
    relations = [model_relation(tenzing_existing_path, tenzing_path)]
    for relation in relations:
        tenzing_existing_path.register_relation(relation)


def register_empty_relations():
    relations = [model_relation(tenzing_empty, tenzing_generic)]
    for relation in relations:
        tenzing_empty.register_relation(relation)


register_integer_relations()
register_float_relations()
register_string_relations()
register_datetime_relations()
register_timedelta_relations()
register_bool_relations()
register_geometry_relations()
register_url_relations()
register_path_relations()
register_categorical_relations()
register_complex_relations()
register_object_relations()
register_date_relations()
register_time_relations()
register_existing_path_relations()
register_empty_relations()

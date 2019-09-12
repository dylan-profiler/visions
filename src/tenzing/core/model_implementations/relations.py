from pathlib import Path
from urllib.parse import urlparse

from tenzing.core.model_implementations.types.tenzing_bool import tenzing_bool
from tenzing.core.model_implementations.types.tenzing_float import tenzing_float
from tenzing.core.model_implementations.types.tenzing_geometry import tenzing_geometry
from tenzing.core.model_implementations.types.tenzing_path import tenzing_path
from tenzing.core.model_implementations.types.tenzing_string import tenzing_string
from tenzing.core.model_implementations.types.tenzing_integer import tenzing_integer
from tenzing.core.model_implementations.types.tenzing_datetime import tenzing_datetime
from tenzing.core.model_implementations.types.tenzing_url import tenzing_url
from tenzing.core.models import model_relation
from tenzing.utils import test_utils
import logging
import pandas as pd


def register_integer_relations():
    relations = [
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

    relations = [model_relation(tenzing_float, tenzing_string, test_string_is_float)]
    for relation in relations:
        tenzing_float.register_relation(relation)


def register_string_relations():
    relations = []
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
        )
    ]
    for relation in relations:
        tenzing_path.register_relation(relation)


def register_datetime_relations():
    relations = [
        model_relation(
            tenzing_datetime,
            tenzing_string,
            test_utils.coercion_test(lambda s: pd.to_datetime(s)),
        )
    ]
    for relation in relations:
        tenzing_datetime.register_relation(relation)


def register_geometry_relations():
    def string_is_geometry(series):
        """
            Shapely logs failures at a silly severity, just trying to suppress it's output on failures.
        """
        from shapely import wkt

        logging.disable(logging.WARNING)
        try:
            result = all(wkt.loads(value) for value in series)
        except Exception:
            result = False
        finally:
            logging.disable(logging.NOTSET)

        return result

    relations = [model_relation(tenzing_geometry, tenzing_string, string_is_geometry)]
    for relation in relations:
        tenzing_geometry.register_relation(relation)


def register_bool_relations():
    class string_bool_relation:
        _boolean_maps = [
            {"true": True, "false": False},
            {"y": True, "n": False},
            {"yes": True, "no": False},
        ]

        # TODO: ensure that series.str.lower() has no side effects
        def string_is_bool(self, series):
            return any(
                [
                    series.str.lower().isin(boolean_map.keys()).all()
                    for boolean_map in self._boolean_maps
                ]
            )

        def map_string_to_bool(self, series):
            return (
                series.str.lower()
                .copy()
                .map({k: v for d in self._boolean_maps for k, v in d.items()})
            )

    sb_relation = string_bool_relation()
    relations = [
        model_relation(
            tenzing_bool,
            tenzing_string,
            sb_relation.string_is_bool,
            sb_relation.map_string_to_bool,
        )
    ]
    for relation in relations:
        tenzing_bool.register_relation(relation)


register_integer_relations()
register_float_relations()
register_string_relations()
register_datetime_relations()
register_bool_relations()
register_geometry_relations()
register_url_relations()
register_path_relations()

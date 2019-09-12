import pandas as pd
import numpy as np
from shapely import wkt

from tenzing.core.model_implementations import *

_test_suite = [
    pd.Series(range(10)),
    pd.Series(range(20)).astype("str"),
    pd.Series(["1.0", "2.0", np.nan]),
    pd.Series(["True", "False"]),
    pd.Series(["True", "False", np.nan]),
    pd.Series(["1.0", "45.67", np.nan]),
    pd.Series(["To travel,", "to experience and learn:", "that is to live"]),
    pd.Series(["To travel,", "to experience and learn:", "that is to live", np.nan]),
    pd.Series(["1988-09-19", "16/4/1987"]),
    pd.Series(range(5)).astype("float"),
    pd.Series([1.0, 2.0, 3.35]),
    pd.Series([True, False]),
    pd.Series([True, False], dtype="category"),
    pd.Series(["2013-7-12", "1/1/2016"]),
    pd.Series([pd.datetime(2017, 1, 1), pd.datetime(2019, 3, 8)]),
    pd.Series(["POINT (12 42)", "POINT (100 42.723)"]),
    pd.Series([wkt.loads("POINT (12 42)"), wkt.loads("POINT (100 42.723)")]),
    pd.Series([pd.datetime(2017, 1, 1), 1.0, "tenzing was a baws"]),
]


def relations_test(source_type, relation_type, test_set=_test_suite):
    relation = source_type.get_relations()[relation_type]
    for test_series in test_set:
        if test_series in relation_type and relation.is_relation(test_series):
            cast_series = relation.transform(test_series)
            assert (
                cast_series in source_type
            ), f"Relationship {relation} cast {test_series.values} to {cast_series.values} "


def test_integer_float_relations():
    relations_test(tenzing_integer, tenzing_float)


def test_integer_string_relations():
    relations_test(tenzing_integer, tenzing_string)


def test_float_string_relations():
    # Since I've carved a hole out of the set of float for Option[Int], casting is now slightly discontinuous
    # where tenzing_float.cast(Series[Option[Int]]) -> tenzing_integer not tenzing_float
    tests = [pd.Series(["1.1", "2"]), pd.Series(["1.1", "2", "NAN", "N/A"])]
    relations_test(tenzing_float, tenzing_string, tests)


def test_timestamp_string_relations():
    relations_test(tenzing_datetime, tenzing_string)


def test_geometry_string_relations():
    relations_test(tenzing_geometry, tenzing_string)


def test_bool_string_relations():
    relations_test(tenzing_bool, tenzing_string)

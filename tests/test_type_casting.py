import pandas as pd
import numpy as np
from shapely import wkt

from tenzing.core.model_implementations import *

_test_suite = [
    pd.Series(range(10)),
    pd.Series(range(20)).astype('str'),
    pd.Series(['1.0', '2.0', np.nan]),
    pd.Series(["True", "False"]),
    pd.Series(["True", "False", np.nan]),
    pd.Series(['1.0', '45.67', np.nan]),
    pd.Series(["To travel,", "to experience and learn:", "that is to live"]),
    pd.Series(["To travel,", "to experience and learn:", "that is to live", np.nan]),
    pd.Series(['1988-09-19', '16/4/1987']),
    pd.Series(range(5)).astype('float'),
    pd.Series([1.0, 2.0, 3.35]),
    pd.Series([True, False]),
    pd.Series([True, False], dtype='category'),
    pd.Series([pd.datetime(2017, 1, 1), pd.datetime(2019, 3, 8)]),
    pd.Series(['POINT (12 42)', 'POINT (100 42.723)']),
    pd.Series([wkt.loads('POINT (12 42)'), wkt.loads('POINT (100 42.723)')]),
    pd.Series([pd.datetime(2017, 1, 1), 1.0, 'tenzing was a baws']),
]


def relations_test(source_type, relation_type):
    relation = source_type.relations[relation_type]
    for test_series in _test_suite:
        if relation.is_relation(test_series):
            cast_series = relation.transform(test_series)
            assert cast_series in source_type, f'Relationship {relation} cast {test_series.values.tolist()} to {cast_series.values.tolist()} '


def test_integer_float_relations_test():
    relations_test(tenzing_integer, tenzing_float)


def test_integer_float_relations_test():
    relations_test(tenzing_integer, tenzing_string)

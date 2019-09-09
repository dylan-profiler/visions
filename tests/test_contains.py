from pathlib import Path
from urllib.parse import urlparse

import pytest
import pandas as pd
import numpy as np
from shapely import wkt

from tenzing.core.model_implementations import *

_test_suite = [
    # Int Series
    pd.Series([1, 2, 3], name='int_series'),
    pd.Series([1, 2, 3], name='categorical_int_series', dtype='category'),
    pd.Series([1, 2, np.nan], name='int_nan_series'),
    pd.Series([1, 2, 3], name='Int64_int_series', dtype='Int64'),
    pd.Series([1, 2, 3, np.nan], name='Int64_int_nan_series', dtype='Int64'),
    pd.Series(np.array([1, 2, 3, 4], dtype=np.uint32), name='np_uint32'),

    # Float Series
    pd.Series([1.0, 2.1, 3.0], name='float_series'),
    pd.Series([1.0, 2.5, np.nan], name='float_nan_series'),
    pd.Series([1.1, 2, 3, 4], name='float_series2'),
    pd.Series(np.array([1.2, 2, 3, 4], dtype=np.float), name='float_series3'),
    pd.Series([1, 2, 3.05, 4], dtype=float, name='float_series4'),
    pd.Series([np.nan, 1.2], name='float_series5'),
    pd.Series([np.nan, 1.1], dtype=np.single, name='float_series6'),
    pd.Series([1.0, 2.0, 3.1], dtype='category', name='categorical_float_series'),

    # String Series
    pd.Series(['hello', 'world'], name='string_series'),
    pd.Series(['hello', 'world'], dtype='category', name='categorical_string_series'),
    pd.Series(['2017-10-01', '12/05/2017'], name='timestamp_string_series'),

    # Bool Series
    pd.Series([True, False], name='bool_series'),
    pd.Series([True, False, np.nan], name='bool_nan_series'),
    pd.Series([True, False, False, True], dtype=bool, name='bool_series2'),
    pd.Series(np.array([1, 0, 0, 1], dtype=np.bool), name='bool_series3'),

    # Complex Series
    pd.Series([np.complex(0, 0), np.complex(1, 2), np.complex(3, -1), np.nan], name='complex_series'),
    pd.Series([np.complex(0, 0), np.complex(1, 2), np.complex(3, -1), np.nan], name='categorical_complex_series',
              dtype='category'),
    pd.Series([complex(0, 0), complex(1, 2), complex(3, -1), np.nan], name='complex_series_py_nan'),
    pd.Series([complex(0, 0), complex(1, 2), complex(3, -1)], name='complex_series_py'),

    # Datetime Series
    pd.Series([pd.datetime(2017, 3, 5), pd.datetime(2019, 12, 4)], name='timestamp_series'),

    # Timedelta Series
    pd.Series([pd.Timedelta(days=i) for i in range(3)], name='timedelta_series'),

    # Geometry Series
    pd.Series(['POINT (-92 42)', 'POINT (-92 42.1)', 'POINT (-92 42.2)'], name='geometry_string_series'),
    pd.Series([wkt.loads('POINT (-92 42)'), wkt.loads('POINT (-92 42.1)'),
               wkt.loads('POINT (-92 42.2)')], name='geometry_series'),

    # Path Series
    pd.Series([Path('/home/user/file.txt'), Path('/home/user/test2.txt')], name='path_series'),

    # Url Series
    pd.Series([urlparse('http://www.cwi.nl:80/%7Eguido/Python.html'), urlparse('https://github.com/pandas-profiling/pandas-profiling')], name='url_series'),
]


def make_pytest_parameterization(true_series):
    def mark_pytest_param(item):
        mark = pytest.mark.basic() if (item.name in true_series) else pytest.mark.xfail()
        return pytest.param(item, marks=mark, id=item.name)
    test_marks = [mark_pytest_param(item) for item in _test_suite]
    return pytest.mark.parametrize('series', test_marks)


@pytest.fixture(params=_test_suite, ids=lambda series: series.name)
def test_series(request):
    yield request.param


@make_pytest_parameterization(['int_series', 'int_nan_series', 'Int64_int_series', 'Int64_int_nan_series', 'np_uint32'])
def test_int_contains(series):
    type = tenzing_integer
    assert series in type


@make_pytest_parameterization(['path_series'])
def test_int_contains(series):
    type = tenzing_path
    assert series in type


@make_pytest_parameterization(['url_series'])
def test_int_contains(series):
    type = tenzing_url
    assert series in type


@make_pytest_parameterization(['float_series', 'float_series2', 'float_series3', 'float_series4', 'float_series5', 'float_series6', 'float_nan_series'])
def test_float_contains(series):
    type = tenzing_float
    assert series in type


@make_pytest_parameterization(['categorical_int_series', 'categorical_float_series', 'categorical_string_series',
                               'categorical_complex_series'])
def test_categorical_contains(series):
    type = tenzing_categorical
    assert series in type


@make_pytest_parameterization(['bool_series', 'bool_series2', 'bool_series3', 'bool_nan_series'])
def test_bool_contains(series):
    type = tenzing_bool
    assert series in type


@make_pytest_parameterization(['complex_series', 'complex_series_py_nan', 'complex_series_py'])
def test_complex_contains(series):
    type = tenzing_complex
    assert series in type


@make_pytest_parameterization(['timestamp_series'])
def test_timestamp_contains(series):
    type = tenzing_timestamp
    assert series in type


@make_pytest_parameterization(['timedelta_series'])
def test_timedelta_contains(series):
    type = tenzing_timedelta
    assert series in type


@make_pytest_parameterization(['timestamp_string_series', 'string_series', 'geometry_string_series'])
def test_string_contains(series):
    type = tenzing_string
    assert series in type


@make_pytest_parameterization(['geometry_series'])
def test_geometry_contains(series):
    type = tenzing_geometry
    assert series in type

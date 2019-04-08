import pytest
import pandas as pd
import numpy as np
from shapely import wkt

from tenzing.core.model_implementations import *

_test_suite = [
    pd.Series([1, 2, 3], name='int_series'),
    pd.Series([1, 2, 3], name='categorical_int_series', dtype='category'),
    pd.Series([1, 2, np.nan], name='int_nan_series'),

    pd.Series([1.0, 2.1, 3.0], name='float_series'),
    pd.Series([1.0, 2.5, np.nan], name='float_nan_series'),
    pd.Series([1.0, 2.0, 3.1], dtype='category', name='categorical_float_series'),

    pd.Series(['hello', 'world'], name='string_series'),
    pd.Series(['hello', 'world'], dtype='category', name='categorical_string_series'),
    pd.Series(['2017-10-01', '12/05/2017'], name='timestamp_string_series'),

    pd.Series([True, False], name='bool_series'),

    pd.Series([np.complex(0, 0), np.complex(1, 2), np.complex(3, -1), np.nan], name='complex_series'),
    pd.Series([np.complex(0, 0), np.complex(1, 2), np.complex(3, -1), np.nan], name='categorical_complex_series',
              dtype='category'),

    pd.Series([pd.datetime(2017, 3, 5), pd.datetime(2019, 12, 4)], name='timestamp_series'),

    pd.Series(['POINT (-92 42)', 'POINT (-92 42.1)', 'POINT (-92 42.2)'], name='geometry_string_series'),
    pd.Series([wkt.loads('POINT (-92 42)'), wkt.loads('POINT (-92 42.1)'),
               wkt.loads('POINT (-92 42.2)')], name='geometry_series'),
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


@make_pytest_parameterization(['int_series', 'int_nan_series'])
def test_int_contains(series):
    type = tenzing_integer
    assert series in type


@make_pytest_parameterization(['float_series', 'float_nan_series'])
def test_float_contains(series):
    type = tenzing_float
    assert series in type


@make_pytest_parameterization(['categorical_int_series', 'categorical_float_series', 'categorical_string_series',
                               'categorical_complex_series'])
def test_categorical_contains(series):
    type = tenzing_categorical
    assert series in type


@make_pytest_parameterization(['bool_series'])
def test_bool_contains(series):
    type = tenzing_bool
    assert series in type


@make_pytest_parameterization(['complex_series'])
def test_complex_contains(series):
    type = tenzing_complex
    assert series in type


@make_pytest_parameterization(['timestamp_series'])
def test_timestamp_contains(series):
    type = tenzing_timestamp
    assert series in type


@make_pytest_parameterization(['timestamp_string_series', 'string_series', 'geometry_string_series'])
def test_string_contains(series):
    type = tenzing_string
    assert series in type


@make_pytest_parameterization(['geometry_series'])
def test_geometry_contains(series):
    type = tenzing_geometry
    assert series in type

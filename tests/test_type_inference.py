from tenzing.core.model_implementations.typesets import (
    tenzing_geometry_set,
    tenzing_standard,
)
from tenzing.core.typesets import infer_type, traverse_relation_graph
from tenzing.core.model_implementations import *
import pandas as pd
import numpy as np
from shapely import wkt


int_series = pd.Series(range(10))

int_string_series = pd.Series(range(20)).astype("str")
int_string_nan_series = pd.Series(["1.0", "2.0", np.nan])
bool_string_series = pd.Series(["True", "False"])
string_bool_nan_series = pd.Series(["True", "False", np.nan])
float_string_series = pd.Series(["1.0", "45.67", np.nan])
string_series = pd.Series(["To travel,", "to experience and learn:", "that is to live"])
string_nan_series = pd.Series(
    ["To travel,", "to experience and learn:", "that is to live", np.nan]
)

timestamp_string_series = pd.Series(["1988-09-19", "16/4/1987"])

int_float_series = pd.Series(range(5)).astype("float")  # long enough to not be cat
float_series = pd.Series([1.0, 2.0, 3.35])

bool_series = pd.Series([True, False])
categorical_bool_series = pd.Series([True, False], dtype="category")

timestamp_series = pd.Series([pd.datetime(2017, 1, 1), pd.datetime(2019, 3, 8)])

geometry_string_series = pd.Series(["POINT (12 42)", "POINT (100 42.723)"])
geometry_series = pd.Series(
    [wkt.loads("POINT (12 42)"), wkt.loads("POINT (100 42.723)")]
)

object_series = pd.Series([pd.datetime(2017, 1, 1), 1.0, "tenzing was a baws"])

standard_typeset = tenzing_standard()
geometry_typeset = tenzing_geometry_set()


def standard_typeset_test(series, expected_type):
    series_type = traverse_relation_graph(series, standard_typeset.inheritance_graph)
    print(series_type)
    inferred_type = infer_type(series_type, series, standard_typeset.relation_graph)
    print(inferred_type)
    print(expected_type)
    assert (
        inferred_type is expected_type
    ), f"Inferred type {inferred_type}, expected type {expected_type}"


def geometry_typeset_test(series, expected_type):
    series_type = traverse_relation_graph(series, geometry_typeset.inheritance_graph)
    inferred_type = infer_type(series_type, series, geometry_typeset.relation_graph)
    assert (
        inferred_type is expected_type
    ), f"Inferred type {inferred_type}, expected type {expected_type}"


def test_int_to_int():
    standard_typeset_test(int_series, tenzing_integer)


def test_string_to_int():
    standard_typeset_test(int_string_series, tenzing_integer)


def test_string_with_nan_int():
    standard_typeset_test(int_string_nan_series, tenzing_integer + missing)


def test_string_to_bool():
    standard_typeset_test(bool_string_series, tenzing_bool)


def test_object_to_float():
    standard_typeset_test(float_string_series, tenzing_float + missing)


def test_object_to_object():
    standard_typeset_test(object_series, tenzing_object)


def test_object_to_timestamp():
    standard_typeset_test(timestamp_string_series, tenzing_datetime)


def test_float_to_int():
    standard_typeset_test(int_float_series, tenzing_integer)


def test_float_to_float():
    standard_typeset_test(float_series, tenzing_float)


def test_bool_to_bool():
    standard_typeset_test(bool_series, tenzing_bool)


def test_timestamp_to_timestamp():
    standard_typeset_test(timestamp_series, tenzing_datetime)


def test_string_bool_nan_to_bool():
    standard_typeset_test(string_bool_nan_series, tenzing_bool + missing)


def test_string_to_float():
    standard_typeset_test(float_string_series, tenzing_float + missing)


def test_string_to_string():
    standard_typeset_test(string_series, tenzing_string)


def test_string_nan_to_string():
    standard_typeset_test(string_nan_series, tenzing_string + missing)


def test_geometry_to_geometry():
    geometry_typeset_test(geometry_series, tenzing_geometry)


def test_string_to_geometry():
    geometry_typeset_test(geometry_string_series, tenzing_geometry)

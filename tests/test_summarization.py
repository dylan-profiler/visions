import pytest
import pandas as pd
import numpy as np

from tenzing.core.model_implementations import (
    tenzing_bool,
    tenzing_integer,
    tenzing_float,
    tenzing_categorical,
    tenzing_complex,
    tenzing_datetime,
    tenzing_time,
    tenzing_date,
    tenzing_object,
    tenzing_string,
    tenzing_geometry,
    missing,
    infinite,
)
from tenzing.core.summary import type_summary_ops, Summary


def validate_summary_output(test_series, tenzing_type, correct_output):
    summary = Summary(type_summary_ops)
    trial_output = summary.summarize_series(test_series, tenzing_type)

    for metric, result in correct_output.items():
        assert metric in trial_output, f"Metric `{metric}` is missing"
        assert (
            trial_output[metric] == result
        ), f"Expected value {result} for metric `{metric}`, got {trial_output[metric]}"


def test_integer_missing_summary(tenzing_type=tenzing_integer):
    tenzing_type += missing
    test_series = pd.Series([0, 1, 2, 3, 4, np.nan])
    correct_output = {
        "n_unique": 5,
        "mean": 2,
        "median": 2,
        "std": pytest.approx(1.58113, 0.00001),
        "max": 4,
        "min": 0,
        "n_records": 6,
        "n_zeros": 1,
        "perc_zeros": 1.0 / 5.0,
        "na_count": 1,
        "perc_na": 1.0 / 6.0,
    }

    validate_summary_output(test_series, tenzing_type, correct_output)


def test_float_missing_summary(tenzing_type=tenzing_float):
    tenzing_type += missing
    test_series = pd.Series([0.0, 1.0, 2.0, 3.0, 4.0, np.nan])
    correct_output = {
        "n_unique": 5,
        "perc_unique": 1.0,
        "median": 2,
        "mean": 2,
        "std": pytest.approx(1.58113, 0.00001),
        "max": 4,
        "min": 0,
        "n_records": 6,
        "n_zeros": 1,
        "perc_zeros": 1 / 5.0,
        "na_count": 1,
        "perc_na": 1.0 / 6.0,
    }

    validate_summary_output(test_series, tenzing_type, correct_output)


def test_bool_missing_summary(tenzing_type=tenzing_bool):
    tenzing_type += missing
    test_series = pd.Series([True, False, True, True, np.nan])
    correct_output = {
        "n_records": 5,
        "na_count": 1,
        "perc_na": 0.2,
        # 'num_True': 3,
        # 'num_False': 1,
        # 'perc_True': 0.75,
        # 'perc_False': 0.25
    }

    validate_summary_output(test_series, tenzing_type, correct_output)


def test_categorical_missing_summary(tenzing_type=tenzing_categorical):
    tenzing_type += missing
    test_series = pd.Series(
        pd.Categorical(
            [True, False, np.nan, "test"], categories=[True, False, "test", "missing"]
        )
    )
    correct_output = {
        "n_unique": 3,
        "n_records": 4,
        "na_count": 1,
        "perc_na": 0.25,
        "category_size": 4,
        "missing_categorical_values": True,
    }

    validate_summary_output(test_series, tenzing_type, correct_output)


def test_complex_missing_summary(tenzing_type=tenzing_complex):
    tenzing_type += missing
    test_series = pd.Series([0 + 0j, 0 + 1j, 1 + 0j, 1 + 1j, np.nan])
    correct_output = {"n_unique": 4, "mean": 0.5 + 0.5j, "na_count": 1, "perc_na": 0.2}

    validate_summary_output(test_series, tenzing_type, correct_output)


def test_datetime_missing_summary(tenzing_type=tenzing_datetime):
    tenzing_type += missing
    test_series = pd.Series(
        [
            pd.datetime(2010, 1, 1),
            pd.datetime(2010, 8, 2),
            pd.datetime(2011, 2, 1),
            np.nan,
        ]
    )
    correct_output = {
        "n_unique": 3,
        "max": pd.datetime(2011, 2, 1),
        "min": pd.datetime(2010, 1, 1),
        "n_records": 4,
        "perc_unique": 1,
        "na_count": 1,
        "perc_na": 0.25,
        "range": test_series.max() - test_series.min(),
    }

    validate_summary_output(test_series, tenzing_type, correct_output)


def test_object_missing_summary(tenzing_type=tenzing_object):
    tenzing_type += missing
    test_series = pd.Series([pd.datetime(2010, 1, 1), "test", 3, np.nan])
    correct_output = {
        "n_unique": 3,
        "frequencies": {"test": 1, 3: 1, pd.datetime(2010, 1, 1): 1},
        "n_records": 4,
        "na_count": 1,
        "perc_na": 0.25,
    }

    validate_summary_output(test_series, tenzing_type, correct_output)


def test_geometry_missing_summary(tenzing_type=tenzing_geometry):
    tenzing_type += missing
    test_series = pd.Series([np.nan])
    correct_output = {"na_count": 1, "perc_na": 1}

    validate_summary_output(test_series, tenzing_type, correct_output)


def test_string_missing_summary(tenzing_type=tenzing_string):
    tenzing_type += missing
    test_series = pd.Series(["apple", "orange", "bike", np.nan])
    correct_output = {"na_count": 1, "perc_na": 0.25}

    validate_summary_output(test_series, tenzing_type, correct_output)


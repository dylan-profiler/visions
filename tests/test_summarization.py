import datetime
from urllib.parse import urlparse

import numpy as np
import pandas as pd
import pytest

from visions.application.summaries import CompleteSummary
from visions.types import (
    URL,
    Boolean,
    Categorical,
    Complex,
    DateTime,
    Float,
    Geometry,
    Integer,
    Object,
    String,
)


@pytest.fixture(scope="class")
def summary():
    return CompleteSummary()


def validate_summary_output(test_series, visions_type, correct_output, summary):
    trial_output = summary.summarize_series(test_series, visions_type)

    for metric, result in correct_output.items():
        assert metric in trial_output, "Metric `{metric}` is missing".format(
            metric=metric
        )

        if isinstance(trial_output[metric], pd.Series):
            trial_output[metric] = trial_output[metric].to_dict()

        assert (
            trial_output[metric] == result
        ), "Expected value {result} for metric `{metric}`, got {output}".format(
            result=result, metric=metric, output=trial_output[metric]
        )


def test_integer_summary(summary, visions_type=Integer):
    test_series = pd.Series([0, 1, 2, 3, 4])
    correct_output = {
        "n_unique": 5,
        "mean": 2,
        "median": 2,
        "std": pytest.approx(1.58113, 0.00001),
        "max": 4,
        "min": 0,
        "n_records": 5,
        "n_zeros": 1,
    }

    validate_summary_output(test_series, visions_type, correct_output, summary)


def test_integer_missing_summary(summary, visions_type=Integer):
    test_series = pd.Series([0, 1, 2, 3, 4])
    correct_output = {
        "n_unique": 5,
        "mean": 2,
        "median": 2,
        "std": pytest.approx(1.58113, 0.00001),
        "max": 4,
        "min": 0,
        "n_records": 5,
        "n_zeros": 1,
        "na_count": 0,
    }

    validate_summary_output(test_series, visions_type, correct_output, summary)


def test_float_missing_summary(summary, visions_type=Float):
    test_series = pd.Series([0.0, 1.0, 2.0, 3.0, 4.0, np.nan])
    correct_output = {
        "n_unique": 5,
        "median": 2,
        "mean": 2,
        "std": pytest.approx(1.58113, 0.00001),
        "max": 4,
        "min": 0,
        "n_records": 6,
        "n_zeros": 1,
        "na_count": 1,
    }

    validate_summary_output(test_series, visions_type, correct_output, summary)


def test_bool_missing_summary(summary, visions_type=Boolean):
    test_series = pd.Series([True, False, True, True, np.nan])
    correct_output = {"n_records": 5, "na_count": 1}

    validate_summary_output(test_series, visions_type, correct_output, summary)


def test_categorical_missing_summary(summary, visions_type=Categorical):
    test_series = pd.Series(
        pd.Categorical(
            [True, False, np.nan, "test"],
            categories=[True, False, "test", "missing"],
            ordered=True,
        )
    )
    correct_output = {
        "n_unique": 3,
        "n_records": 4,
        "na_count": 1,
        "category_size": 4,
        "missing_categorical_values": True,
    }

    validate_summary_output(test_series, visions_type, correct_output, summary)


def test_complex_missing_summary(summary, visions_type=Complex):
    test_series = pd.Series([0 + 0j, 0 + 1j, 1 + 0j, 1 + 1j, np.nan])
    correct_output = {"n_unique": 4, "mean": 0.5 + 0.5j, "na_count": 1, "n_records": 5}

    validate_summary_output(test_series, visions_type, correct_output, summary)


def test_datetime_missing_summary(summary, visions_type=DateTime):
    test_series = pd.Series(
        [
            datetime.datetime(2010, 1, 1),
            datetime.datetime(2010, 8, 2),
            datetime.datetime(2011, 2, 1),
            np.nan,
        ]
    )
    correct_output = {
        "n_unique": 3,
        "max": datetime.datetime(2011, 2, 1),
        "min": datetime.datetime(2010, 1, 1),
        "n_records": 4,
        "na_count": 1,
        "range": test_series.max() - test_series.min(),
    }

    validate_summary_output(test_series, visions_type, correct_output, summary)


def test_object_missing_summary(summary, visions_type=Object):
    test_series = pd.Series([datetime.datetime(2010, 1, 1), "test", 3, np.nan])
    correct_output = {
        "n_unique": 3,
        "frequencies": {"test": 1, 3: 1, datetime.datetime(2010, 1, 1): 1},
        "n_records": 4,
        "na_count": 1,
    }

    validate_summary_output(test_series, visions_type, correct_output, summary)


def test_geometry_missing_summary(summary, visions_type=Geometry):
    test_series = pd.Series([np.nan])
    correct_output = {"na_count": 1, "n_records": 1}

    validate_summary_output(test_series, visions_type, correct_output, summary)


def test_string_missing_summary(summary, visions_type=String):
    test_series = pd.Series(["apple", "orange", "bike", np.nan])
    correct_output = {"na_count": 1, "n_unique": 3, "n_records": 4}

    validate_summary_output(test_series, visions_type, correct_output, summary)


def test_string_summary(summary, visions_type=String):
    test_series = pd.Series(["http://ru.nl", "http://ru.nl", "http://nl.ru"])
    correct_output = {"n_unique": 2, "n_records": 3}

    validate_summary_output(test_series, visions_type, correct_output, summary)


def test_string_empty_summary(summary, visions_type=String):
    test_series = pd.Series(["", "", ""])
    correct_output = {"n_unique": 1, "n_records": 3}

    validate_summary_output(test_series, visions_type, correct_output, summary)


def test_url_summary(summary, visions_type=URL):
    test_series = pd.Series(
        [urlparse("http://ru.nl"), urlparse("http://ru.nl"), urlparse("http://nl.ru")]
    )
    correct_output = {
        "n_records": 3,
        "n_unique": 2,
        "scheme_counts": {"http": 3},
        "netloc_counts": {"ru.nl": 2, "nl.ru": 1},
        "path_counts": {"": 3},
        "query_counts": {"": 3},
        "fragment_counts": {"": 3},
    }

    validate_summary_output(test_series, visions_type, correct_output, summary)


def test_empty_summary():
    pass

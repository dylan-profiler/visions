import numpy as np
import pandas as pd

from visions.application.summaries import CompleteSummary
from visions.application.summaries.functional import (
    summarize,
    summarize_frame,
    summarize_series,
)
from visions.types import Integer, String


def test_summarize_frame():
    df = pd.DataFrame(
        {
            "Brand": ["Honda Civic", "Toyota Corolla", "Ford Focus", "Audi A4"],
            "Price": [22000, 25000, 27000, 35000],
        },
        columns=["Brand", "Price"],
    )
    summary = summarize_frame(
        df, {"Brand": String, "Price": Integer}, CompleteSummary()
    )
    summary.pop("type_counts")
    assert summary == {
        "n_observations": 4,
        "n_variables": 2,
        "memory_size": 430,
        "na_count": 0,
        "n_vars_missing": 0,
    }


def test_summarize_series():
    brand_series = pd.Series(["Honda Civic", "Toyota Corolla", "Ford Focus", "Audi A4"])

    summary = summarize_series(brand_series, String, CompleteSummary())

    assert summary["n_unique"] == 4
    assert summary["length"].to_dict() == {0: 11, 1: 14, 2: 10, 3: 7}
    assert summary["max_length"] == 14
    assert summary["min_length"] == 7
    assert summary["mean_length"] == 10.5
    assert summary["median_length"] == 10.5
    assert summary["n_characters"] == 20

    assert summary["category_alias_values"] == {
        "H": "Uppercase_Letter",
        "o": "Lowercase_Letter",
        "n": "Lowercase_Letter",
        "d": "Lowercase_Letter",
        "a": "Lowercase_Letter",
        " ": "Space_Separator",
        "C": "Uppercase_Letter",
        "i": "Lowercase_Letter",
        "v": "Lowercase_Letter",
        "c": "Lowercase_Letter",
        "T": "Uppercase_Letter",
        "y": "Lowercase_Letter",
        "t": "Lowercase_Letter",
        "r": "Lowercase_Letter",
        "l": "Lowercase_Letter",
        "F": "Uppercase_Letter",
        "u": "Lowercase_Letter",
        "s": "Lowercase_Letter",
        "A": "Uppercase_Letter",
        "4": "Decimal_Number",
    }

    assert summary["frequencies"] == {
        "Audi A4": 1,
        "Honda Civic": 1,
        "Ford Focus": 1,
        "Toyota Corolla": 1,
    }

    price_series = pd.Series([22000, 25000, 27000, 35000])

    summary = summarize_series(price_series, Integer, CompleteSummary())
    assert summary == {
        "n_infinite": 0,
        "mean": 27250.0,
        "std": 5560.275772537426,
        "variance": 30916666.666666668,
        "max": 35000.0,
        "min": 22000.0,
        "median": 26000.0,
        "kurt": 1.8192544372679649,
        "skew": 1.19978923754086,
        "sum": 109000.0,
        "mad": 2500.0,
        "quantile_5": 22450.0,
        "quantile_25": 24250.0,
        "quantile_50": 26000.0,
        "quantile_75": 29000.0,
        "quantile_95": 33800.0,
        "iqr": 4750.0,
        "range": 13000.0,
        "cv": 0.20404681734082297,
        "n_zeros": 0,
        "is_unique": True,
        "n_unique": 4,
        "frequencies": {27000: 1, 35000: 1, 25000: 1, 22000: 1},
        "n_records": 4,
        "memory_size": 160,
        "dtype": np.int64,
        "types": {"int": 4},
        "na_count": 0,
        "monotonic_decrease": False,
        "monotonic_decrease_strict": False,
        "monotonic_increase": True,
        "monotonic_increase_strict": True,
    }


def test_summarize():
    df = pd.DataFrame(
        {
            "Brand": ["Honda Civic", "Toyota Corolla", "Ford Focus", "Audi A4"],
            "Price": [22000, 25000, 27000, 35000],
        },
        columns=["Brand", "Price"],
    )
    summary = summarize(df, {"Brand": String, "Price": Integer}, CompleteSummary())

    assert summary["types"] == {"Brand": String, "Price": Integer}

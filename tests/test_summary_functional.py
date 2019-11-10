import pandas as pd
import numpy as np

from visions.application.summaries.functional import (
    summarize_frame,
    summarize_series,
    summarize,
)
from visions.application.summaries.summary import CompleteSummary
from visions.core.implementations.types import visions_string, visions_integer


def test_summarize_frame():
    df = pd.DataFrame(
        {
            "Brand": ["Honda Civic", "Toyota Corolla", "Ford Focus", "Audi A4"],
            "Price": [22000, 25000, 27000, 35000],
        },
        columns=["Brand", "Price"],
    )
    summary = summarize_frame(
        df, {"Brand": visions_string, "Price": visions_integer}, CompleteSummary()
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

    summary = summarize_series(brand_series, visions_string, CompleteSummary())
    assert summary == {
        "n_unique": 4,
        "length": {7: 1, 14: 1, 11: 1, 10: 1},
        "category_short_values": {
            "H": "Lu",
            "o": "Ll",
            "n": "Ll",
            "d": "Ll",
            "a": "Ll",
            " ": "Zs",
            "C": "Lu",
            "i": "Ll",
            "v": "Ll",
            "c": "Ll",
            "T": "Lu",
            "y": "Ll",
            "t": "Ll",
            "r": "Ll",
            "l": "Ll",
            "F": "Lu",
            "u": "Ll",
            "s": "Ll",
            "A": "Lu",
            "4": "Nd",
        },
        "category_alias_values": {
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
        },
        "script_values": {
            "H": "Latin",
            "o": "Latin",
            "n": "Latin",
            "d": "Latin",
            "a": "Latin",
            " ": "Common",
            "C": "Latin",
            "i": "Latin",
            "v": "Latin",
            "c": "Latin",
            "T": "Latin",
            "y": "Latin",
            "t": "Latin",
            "r": "Latin",
            "l": "Latin",
            "F": "Latin",
            "u": "Latin",
            "s": "Latin",
            "A": "Latin",
            "4": "Common",
        },
        "block_values": {
            "H": "Basic Latin",
            "o": "Basic Latin",
            "n": "Basic Latin",
            "d": "Basic Latin",
            "a": "Basic Latin",
            " ": "Basic Latin",
            "C": "Basic Latin",
            "i": "Basic Latin",
            "v": "Basic Latin",
            "c": "Basic Latin",
            "T": "Basic Latin",
            "y": "Basic Latin",
            "t": "Basic Latin",
            "r": "Basic Latin",
            "l": "Basic Latin",
            "F": "Basic Latin",
            "u": "Basic Latin",
            "s": "Basic Latin",
            "A": "Basic Latin",
            "4": "Basic Latin",
        },
        "block_alias_values": {
            "H": "ASCII",
            "o": "ASCII",
            "n": "ASCII",
            "d": "ASCII",
            "a": "ASCII",
            " ": "ASCII",
            "C": "ASCII",
            "i": "ASCII",
            "v": "ASCII",
            "c": "ASCII",
            "T": "ASCII",
            "y": "ASCII",
            "t": "ASCII",
            "r": "ASCII",
            "l": "ASCII",
            "F": "ASCII",
            "u": "ASCII",
            "s": "ASCII",
            "A": "ASCII",
            "4": "ASCII",
        },
        "frequencies": {
            "Audi A4": 1,
            "Honda Civic": 1,
            "Ford Focus": 1,
            "Toyota Corolla": 1,
        },
        "n_records": 4,
        "memory_size": 398,
        "dtype": np.object_,
        "types": {"str": 4},
        "na_count": 0,
    }

    price_series = pd.Series([22000, 25000, 27000, 35000])

    summary = summarize_series(price_series, visions_integer, CompleteSummary())
    assert summary == {
        "inf_count": 0,
        "mean": 27250.0,
        "std": 5560.275772537426,
        "var": 30916666.666666668,
        "max": 35000.0,
        "min": 22000.0,
        "median": 26000.0,
        "kurt": 1.8192544372679649,
        "skew": 1.19978923754086,
        "sum": 109000.0,
        "mad": 3875.0,
        "quantile_5": 22450.0,
        "quantile_25": 24250.0,
        "quantile_50": 26000.0,
        "quantile_75": 29000.0,
        "quantile_95": 33800.0,
        "iqr": 4750.0,
        "range": 13000.0,
        "cv": 0.20404681734082297,
        "n_zeros": 0,
        "n_unique": 4,
        "frequencies": {27000: 1, 35000: 1, 25000: 1, 22000: 1},
        "n_records": 4,
        "memory_size": 160,
        "dtype": np.int64,
        "types": {"int": 4},
        "na_count": 0,
    }


def test_summarize():
    df = pd.DataFrame(
        {
            "Brand": ["Honda Civic", "Toyota Corolla", "Ford Focus", "Audi A4"],
            "Price": [22000, 25000, 27000, 35000],
        },
        columns=["Brand", "Price"],
    )
    summary = summarize(
        df, {"Brand": visions_string, "Price": visions_integer}, CompleteSummary()
    )

    assert summary["types"] == {"Brand": visions_string, "Price": visions_integer}

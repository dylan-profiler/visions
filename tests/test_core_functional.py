import pandas as pd
import numpy as np

from visions.core.functional import (
    type_inference_frame,
    type_detect_frame,
    type_detect_series,
    type_inference_series,
    type_cast_series,
    type_cast_frame,
)
from visions.core.implementations.types import (
    visions_string,
    visions_integer,
    visions_datetime,
    visions_complex,
)
from visions.core.implementations.typesets import (
    visions_complete_set,
    visions_standard_set,
)


def test_type_inference_frame():
    # Create a DataFrame with various string columns
    df = pd.DataFrame(
        {
            "latin": ["orange", "apple", "pear"],
            "cyrillic": ["Кириллица", "гласность", "демократија"],
            "mixed": ["Кириллица", "soep", "демократија"],
            "burmese": ["ရေကြီးခြင်း", "စက်သင်ယူမှု", "ဉာဏ်ရည်တု"],
            "digits": ["01234", "121223", "12312"],
            "specials": ["$", "%^&*(", "!!!~``"],
            "whitespace": ["\t", "\n", " "],
            "jiddisch": ["רעכט צו לינקס", "שאָסיי 61", "פּיצאַ איז אָנגענעם"],
            "arabic": ["بوب ديلان", "باتي فالنتين", "السيد الدف الرجل"],
            "playing_cards": ["🂶", "🃁", "🂻"],
        }
    )

    # Initialize the typeset
    typeset = visions_complete_set()

    # Infer the column type
    types = type_inference_frame(df, typeset)
    assert types == {
        "latin": visions_string,
        "cyrillic": visions_string,
        "mixed": visions_string,
        "burmese": visions_string,
        "digits": visions_integer,
        "specials": visions_string,
        "whitespace": visions_string,
        "jiddisch": visions_string,
        "arabic": visions_string,
        "playing_cards": visions_string,
    }


def test_type_inference_series():
    string_series = pd.Series(["(12.0+10.0j)", "(-4.0+6.2j)", "(8.0+2.0j)"])

    typeset = visions_standard_set()
    detected_type = type_inference_series(string_series, typeset)
    assert detected_type == visions_complex


def test_type_cast_frame():
    df = pd.DataFrame(
        {
            "latin": ["orange", "apple", "pear"],
            "cyrillic": ["Кириллица", "гласность", "демократија"],
            "mixed": ["Кириллица", "soep", "демократија"],
            "burmese": ["ရေကြီးခြင်း", "စက်သင်ယူမှု", "ဉာဏ်ရည်တု"],
            "digits": ["01234", "121223", "12312"],
            "specials": ["$", "%^&*(", "!!!~``"],
            "whitespace": ["\t", "\n", " "],
            "jiddisch": ["רעכט צו לינקס", "שאָסיי 61", "פּיצאַ איז אָנגענעם"],
            "arabic": ["بوب ديلان", "باتي فالنتين", "السيد الدف الرجل"],
            "playing_cards": ["🂶", "🃁", "🂻"],
        }
    )

    typeset = visions_complete_set()
    new_df = type_cast_frame(df, typeset)
    assert new_df["digits"].iloc[1] - 3 == 121220
    assert new_df["latin"].iloc[1] + "1" == "apple1"


def test_type_cast_series():
    string_series = pd.Series(["(12.0+10.0j)", "(-4.0+6.2j)", "(8.0+2.0j)"])

    typeset = visions_standard_set()
    new_series = type_cast_series(string_series, typeset)
    assert new_series.iloc[1].real == -4.0


def test_type_detect_frame():
    # Create a DataFrame with various string columns
    df = pd.DataFrame(
        {
            "latin": ["orange", "apple", "pear"],
            "cyrillic": ["Кириллица", "гласность", "демократија"],
            "mixed": ["Кириллица", "soep", "демократија"],
            "burmese": ["ရေကြီးခြင်း", "စက်သင်ယူမှု", "ဉာဏ်ရည်တု"],
            "digits": ["01234", "121223", "12312"],
            "specials": ["$", "%^&*(", "!!!~``"],
            "whitespace": ["\t", "\n", " "],
            "jiddisch": ["רעכט צו לינקס", "שאָסיי 61", "פּיצאַ איז אָנגענעם"],
            "arabic": ["بوب ديلان", "باتي فالنتين", "السيد الدف الرجل"],
            "playing_cards": ["🂶", "🃁", "🂻"],
        }
    )

    # Initialize the typeset
    typeset = visions_complete_set()

    # Infer the column type
    types = type_detect_frame(df, typeset)
    assert types == {
        "latin": visions_string,
        "cyrillic": visions_string,
        "mixed": visions_string,
        "burmese": visions_string,
        "digits": visions_string,
        "specials": visions_string,
        "whitespace": visions_string,
        "jiddisch": visions_string,
        "arabic": visions_string,
        "playing_cards": visions_string,
    }


def test_type_detect_series():
    datetime_series = pd.Series(
        [
            pd.datetime(2010, 1, 1),
            pd.datetime(2010, 8, 2),
            pd.datetime(2011, 2, 1),
            np.datetime64("NaT"),
        ]
    )

    typeset = visions_standard_set()
    detected_type = type_detect_series(datetime_series, typeset)
    assert detected_type == visions_datetime

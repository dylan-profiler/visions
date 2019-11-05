import pandas as pd

from visions.core.functional import type_inference
from visions.core.implementations.types import visions_string
from visions.core.implementations.typesets import visions_complete_set


def test_type_inference():
    # Create a DataFrame with various string columns
    df = pd.DataFrame(
        {
            "latin": ["orange", "apple", "pear"],
            "cyrillic": ["Кириллица", "гласность", "демократија"],
            "mixed": ["Кириллица", "soep", "демократија"],
            "burmese": ["ရေကြီးခြင်း", "စက်သင်ယူမှု", "ဉာဏ်ရည်တု"],
            "digits": ["01234", "121223", "123123"],
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
    types = type_inference(df, typeset)
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


def test_type_detect():
    # TODO: complete tests
    raise NotImplementedError()

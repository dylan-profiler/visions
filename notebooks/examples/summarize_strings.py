from visions.core.model.typesets import tenzing_complete_set

import pandas as pd

from visions.core.summaries.summary import summary

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


ts = tenzing_complete_set()
ts.prep(df)

x = summary.summarize(df, ts.column_type_map)
for key, variable_summary in x["series"].items():
    print(key, variable_summary)
    # print(
    #     f"series with name {key} contains the unicode values {variable_summary['unicode_scripts']}"
    # )

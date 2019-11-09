import pandas as pd

from visions.core.functional import type_inference
from visions.core.implementations.typesets import visions_complete_set
from visions.application.summaries.summary import CompleteSummary

# Create a DataFrame with various string columns
df = pd.DataFrame(
    {
        "latin": ["orange", "apple", "pear"],
        "cyrillic": ["Кириллица", "гласность", "демократија"],
        "mixed": ["Кириллица", "soep", "демократија"],
        "burmese": ["ရေကြီးခြင်း", "စက်သင်ယူမှု", "ဉာဏ်ရည်တု"],
        # "digits": ["01234", "121223", "123123"],
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

# Generate a summary
summarizer = CompleteSummary()
summary = summarizer.summarize(df, types)
for key, variable_summary in summary["series"].items():
    print(
        f"Scripts in '{key}' column: {set(variable_summary['script_values'].values())}"
    )

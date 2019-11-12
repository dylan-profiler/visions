import pandas as pd

from visions.core.functional import type_detect_frame
from visions.core.implementations.typesets import visions_complete_set
from visions.application.summaries.summary import CompleteSummary

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
types = type_detect_frame(df, typeset)

# Generate a summary
summarizer = CompleteSummary()
summary = summarizer.summarize(df, types)

print(f"| {'Column': <15}| {'Scripts': <17}| {'Categories': <84}| {'Blocks': <25}|")
print(f"{'':-<17}+{'':-<18}+{'':-<85}+{'':-<26}+")
for column, variable_summary in summary["series"].items():
    scripts = ", ".join(set(variable_summary["script_values"].values()))
    categories = ", ".join(set(variable_summary["category_alias_values"].values()))
    blocks = ", ".join(set(variable_summary["block_values"].values()))

    print(f"| {column: <15}| {scripts: <17}| {categories: <84}| {blocks: <25}|")

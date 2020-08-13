import pandas as pd

from visions.application.summaries import CompleteSummary
from visions.functional import detect_type
from visions.typesets import CompleteSet

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
typeset = CompleteSet()

# Infer the column type
types = detect_type(df, typeset)

# Generate a summary
summarizer = CompleteSummary()
summary = summarizer.summarize(df, types)

print(
    "| {h1: <15}| {h2: <17}| {h3: <84}| {h4: <25}|".format(
        h1="Column", h2="Scripts", h3="Categories", h4="Blocks"
    )
)
print("{e:-<17}+{e:-<18}+{e:-<85}+{e:-<26}+".format(e=""))
for column, variable_summary in summary["series"].items():
    scripts = ", ".join(set(variable_summary["script_values"].values()))
    categories = ", ".join(set(variable_summary["category_alias_values"].values()))
    blocks = ", ".join(set(variable_summary["block_values"].values()))

    print(
        "| {column: <15}| {scripts: <17}| {categories: <84}| {blocks: <25}|".format(
            column=column, scripts=scripts, categories=categories, blocks=blocks
        )
    )

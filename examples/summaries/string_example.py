import pandas as pd

import visions as v
from visions.application.summaries import CompleteSummary

string_series = pd.Series(["orange", "apple", "pear", "🂶", "🃁", "🂻"])

summarizer = CompleteSummary()
summary = summarizer.summarize_series(string_series, v.String)
print(summary)

# Output:
# {
#     "n_unique": 6,
#     "length": {1: 3, 6: 1, 5: 1, 4: 1},
#     "category_short_values": {
#         "o": "Ll",
#         "r": "Ll",
#         "a": "Ll",
#         "n": "Ll",
#         "g": "Ll",
#         "e": "Ll",
#         "p": "Ll",
#         "l": "Ll",
#         "🂶": "So",
#         "🃁": "So",
#         "🂻": "So",
#     },
#     "category_alias_values": {
#         "o": "Lowercase_Letter",
#         "r": "Lowercase_Letter",
#         "a": "Lowercase_Letter",
#         "n": "Lowercase_Letter",
#         "g": "Lowercase_Letter",
#         "e": "Lowercase_Letter",
#         "p": "Lowercase_Letter",
#         "l": "Lowercase_Letter",
#         "🂶": "Other_Symbol",
#         "🃁": "Other_Symbol",
#         "🂻": "Other_Symbol",
#     },
#     "script_values": {
#         "o": "Latin",
#         "r": "Latin",
#         "a": "Latin",
#         "n": "Latin",
#         "g": "Latin",
#         "e": "Latin",
#         "p": "Latin",
#         "l": "Latin",
#         "🂶": "Common",
#         "🃁": "Common",
#         "🂻": "Common",
#     },
#     "block_values": {
#         "o": "Basic Latin",
#         "r": "Basic Latin",
#         "a": "Basic Latin",
#         "n": "Basic Latin",
#         "g": "Basic Latin",
#         "e": "Basic Latin",
#         "p": "Basic Latin",
#         "l": "Basic Latin",
#         "🂶": "Playing Cards",
#         "🃁": "Playing Cards",
#         "🂻": "Playing Cards",
#     },
#     "block_alias_values": {
#         "o": "ASCII",
#         "r": "ASCII",
#         "a": "ASCII",
#         "n": "ASCII",
#         "g": "ASCII",
#         "e": "ASCII",
#         "p": "ASCII",
#         "l": "ASCII",
#         "🂶": "Playing Cards",
#         "🃁": "Playing Cards",
#         "🂻": "Playing Cards",
#     },
#     "frequencies": {"🃁": 1, "orange": 1, "🂶": 1, "pear": 1, "🂻": 1, "apple": 1},
#     "n_records": 6,
#     "memory_size": 593,
#     "dtype": dtype("O"),
#     "types": {"str": 6},
#     "na_count": 0,
# }

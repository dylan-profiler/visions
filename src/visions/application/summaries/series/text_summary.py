from collections import Counter

import pandas as pd
from tangled_up_in_unicode import block, block_abbr, category, category_long, script

from visions.application.summaries.series.numerical_summary import (
    named_aggregate_summary,
)


def get_character_counts(series: pd.Series) -> Counter:
    """Function to return the character counts

    Args:
        series: the Series to process

    Returns:
        A dict with character counts
    """
    return Counter(series.str.cat())


def counter_to_series(counter: Counter) -> pd.Series:
    if not counter:
        return pd.Series()

    counter_as_tuples = counter.most_common()
    items, counts = zip(*counter_as_tuples)
    return pd.Series(counts, index=items)


def unicode_summary(series: pd.Series) -> dict:
    # Unicode Character Summaries (category and script name)
    character_counts = get_character_counts(series)

    character_counts_series = counter_to_series(character_counts)

    char_to_block = {key: block(key) for key in character_counts.keys()}
    char_to_category_short = {key: category(key) for key in character_counts.keys()}
    char_to_script = {key: script(key) for key in character_counts.keys()}

    summary = {
        "n_characters": len(character_counts_series),
        "character_counts": character_counts_series,
        "category_alias_values": {
            key: category_long(value) for key, value in char_to_category_short.items()
        },
        "block_alias_values": {
            key: block_abbr(value) for key, value in char_to_block.items()
        },
    }

    # Retrieve original distribution
    block_alias_counts: Counter = Counter()
    per_block_char_counts: dict = {
        k: Counter() for k in summary["block_alias_values"].values()
    }
    for char, n_char in character_counts.items():
        block_name = summary["block_alias_values"][char]
        block_alias_counts[block_name] += n_char
        per_block_char_counts[block_name][char] = n_char
    summary["block_alias_counts"] = counter_to_series(block_alias_counts)
    summary["block_alias_char_counts"] = {
        k: counter_to_series(v) for k, v in per_block_char_counts.items()
    }

    script_counts: Counter = Counter()
    per_script_char_counts: dict = {k: Counter() for k in char_to_script.values()}
    for char, n_char in character_counts.items():
        script_name = char_to_script[char]
        script_counts[script_name] += n_char
        per_script_char_counts[script_name][char] = n_char
    summary["script_counts"] = counter_to_series(script_counts)
    summary["script_char_counts"] = {
        k: counter_to_series(v) for k, v in per_script_char_counts.items()
    }

    category_alias_counts: Counter = Counter()
    per_category_alias_char_counts: dict = {
        k: Counter() for k in summary["category_alias_values"].values()
    }
    for char, n_char in character_counts.items():
        category_alias_name = summary["category_alias_values"][char]
        category_alias_counts[category_alias_name] += n_char
        per_category_alias_char_counts[category_alias_name][char] += n_char
    summary["category_alias_counts"] = counter_to_series(category_alias_counts)
    summary["category_alias_char_counts"] = {
        k: counter_to_series(v) for k, v in per_category_alias_char_counts.items()
    }

    # Unique counts
    summary["n_category"] = len(summary["category_alias_counts"])
    summary["n_scripts"] = len(summary["script_counts"])
    summary["n_block_alias"] = len(summary["block_alias_counts"])

    return summary


def length_summary(series: pd.Series) -> dict:
    length = series.str.len()
    summary = {"length": length}
    summary.update(named_aggregate_summary(length, "length"))
    return summary


def text_summary(series: pd.Series) -> dict:
    """

    Args:
        series: series to summarize

    Returns:

    """
    # Distribution of length
    summary = {}
    summary.update(length_summary(series))
    summary.update(unicode_summary(series))

    return summary

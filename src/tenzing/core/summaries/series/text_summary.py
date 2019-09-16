from unicodedata import category

import pandas as pd

from tenzing.utils.unicode.unicode_data import script, block, category_alias


def text_summary(series: pd.Series) -> dict:
    """

    Args:
        series:

    Returns:

    """
    # Distribution of length
    summary = {"length": series.map(lambda x: len(str(x))).value_counts().to_dict()}

    # Unicode Character Summaries (category and script name)
    category_values = series.apply(
        lambda sequence: {category(character) for character in sequence}
    )
    summary["category_short_values"] = {y for x in category_values.values for y in x}

    category_long_values = series.apply(
        lambda sequence: {category_alias(character) for character in sequence}
    )
    summary["category_alias_values"] = {
        y for x in category_long_values.values for y in x
    }

    script_values = series.apply(
        lambda sequence: {script(character) for character in sequence}
    )
    summary["script_values"] = {y for x in script_values.values for y in x}

    block_values = series.apply(
        lambda sequence: {block(character) for character in sequence}
    )
    summary["block_values"] = {y for x in block_values.values for y in x}

    return summary

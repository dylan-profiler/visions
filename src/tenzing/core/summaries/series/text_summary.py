import pandas as pd

from tenzing.utils.unicodedata2 import script_cat


def text_summary(series: pd.Series) -> dict:
    """

    Args:
        series:

    Returns:

    """
    # Distribution of length
    summary = {"length": series.map(lambda x: len(str(x))).value_counts().to_dict()}

    # Unicode Scripts and Categories
    unicode_series = series.apply(
        lambda sequence: {script_cat(character) for character in sequence}
    )
    # TODO: add name of category
    # http://www.unicode.org/reports/tr44/#GC_Values_Table
    unicode_scripts = {y for x in unicode_series.values for y in x}
    summary["unicode_scripts"] = unicode_scripts

    return summary

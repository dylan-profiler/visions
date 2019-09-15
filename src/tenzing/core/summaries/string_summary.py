from tenzing.utils.unicodedata2 import script_cat


def string_summary(series):
    # Distribution of length
    summary = {"length": series.map(lambda x: len(str(x))).value_counts().to_dict()}

    # Unicode Scripts and Categories
    unicode_series = series.apply(
        lambda sequence: {script_cat(character) for character in sequence}
    )
    unicode_scripts = {y for x in unicode_series.values for y in x}
    summary["unicode_scripts"] = unicode_scripts

    return summary

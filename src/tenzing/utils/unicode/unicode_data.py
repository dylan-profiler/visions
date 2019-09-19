from functools import partial
from pathlib import Path

import pandas as pd


def parse_range(x: str, pos: int) -> int:
    """ Parse the unicode range to int (base 16)

    Args:
        x: range value
        pos: position to extract

    Returns:

    """
    vals = x.split("..")
    if len(vals) == 1:
        vals.append(vals[0])
    vals = [int(x, 16) for x in vals]
    return vals[pos]


def _parse(set_name):
    file_name = f"data/{set_name}.txt"

    mapping = parse_mapping()
    names = mapping[set_name]

    df = pd.read_csv(
        Path(__file__).parent / file_name,
        sep=";",
        comment="#",
        names=names,
        skipinitialspace=True,
    )
    if "range" in names:
        df["start"] = df["range"].apply(partial(parse_range, pos=0))
        df["end"] = df["range"].apply(partial(parse_range, pos=1))
    elif "idx" in names:
        df["idx"] = df["idx"].apply(partial(int, base=16))

    return df


def parse_mapping():
    mapping = {
        "PropList": ["range", "Property"],
        "DerivedCoreProperties": ["range", "Derived_Property"],
        "Blocks": ["range", "Block"],
        "PropertyValueAliases": [
            "Property",
            "Short_Name",
            "Long_Name",
            "Alternative1",
            "Alternative2",
        ],
        "LineBreak": ["range", "Line_Break"],
        "Scripts": ["range", "Script"],
        "ScriptExtension": ["range", "Script_Extension"],
        "NameAliases": ["idx", "Alias", "Type"],
        "EastAsianWidth": ["range", "East_Asian_Width"],
        "UnicodeData": [
            "idx",
            "name",
            "category",
            "combining",
            "bidirectional",
            "decomposition",
            "decimal",
            "digit",
            "numeric",
            "mirrored",
            "Unicode 1.0 Name",
            "10646 comment field",
            "uppercase",
            "lowercase",
            "titlecase",
        ],
    }
    return mapping


def _lookup(dataset, col, chr, default=None):
    df = _parse(dataset)
    idx = ord(chr)
    try:
        if "idx" in df.columns:
            value = df[df.idx == idx][col]
        elif "start" in df.columns and "end" in df.columns:
            value = df[(df.start <= idx) & (df.end >= idx)][col]
        else:
            raise ValueError('DataFrame misses "idx" or "start" and "end" columns.')

        if len(value) == 1:
            return value.iloc[0]
        elif len(value) > 1:
            return value.values.tolist()
        else:
            raise ValueError("Not found")
    except IndexError:
        if default is None:
            raise ValueError("Character not found.")
        else:
            return default


def _alias(property, short_name):
    df = _parse("PropertyValueAliases")
    df["Property"] = df["Property"].str.strip()
    df["Short_Name"] = df["Short_Name"].str.strip()
    try:
        return df[(df["Property"] == property) & (df["Short_Name"] == short_name)][
            "Long_Name"
        ].iloc[0]
    except IndexError:
        return None


def name(chr, default=None):
    """Returns the name assigned to the character chr as a string. If no name is defined, default is returned, or, if not given, ValueError is raised."""
    return _lookup("UnicodeData", "name", chr, default)


def category(chr):
    """Returns the general category assigned to the character chr as string."""
    return _lookup("UnicodeData", "category", chr, "Zzzz")


def bidirectional(chr):
    """Returns the bidirectional class assigned to the character chr as string. If no such value is defined, an empty string is returned."""
    return _lookup("UnicodeData", "bidirectional", chr, "")


def decimal(chr, default=None):
    """Returns the decimal value assigned to the character chr as integer. If no such value is defined, default is returned, or, if not given, ValueError is raised."""
    return _lookup("UnicodeData", "decimal", chr, default)


def digit(chr, default=None):
    """Returns the digit value assigned to the character chr as integer. If no such value is defined, default is returned, or, if not given, ValueError is raised."""
    return _lookup("UnicodeData", "digit", chr, default)


def numeric(chr, default=None):
    """Returns the numeric value assigned to the character chr as float. If no such value is defined, default is returned, or, if not given, ValueError is raised."""
    return _lookup("UnicodeData", "numeric", chr, default)


def east_asian_width(chr, default=None):
    """Returns the east asian width assigned to the character chr as string."""
    return _lookup("EastAsianWidth", "East_Asian_Width", chr, default).strip()


def combining(chr):
    """Returns the canonical combining class assigned to the character chr as integer. Returns 0 if no combining class is defined."""
    return _lookup("UnicodeData", "combining", chr, 0)


def mirrored(chr):
    """Returns the mirrored property assigned to the character chr as integer. Returns 1 if the character has been identified as a “mirrored” character in bidirectional text, 0 otherwise."""
    return _lookup("UnicodeData", "mirrored", chr, 0)


def decomposition(chr):
    """Returns the character decomposition mapping assigned to the character chr as string. An empty string is returned in case no such mapping is defined."""
    val = _lookup("UnicodeData", "decomposition", chr, 0)
    if str(val) == "nan":
        val = ""
    return val


# Extended functionality
def block(chr):
    return _lookup("Blocks", "Block", chr, "Unknown")


def script(chr):
    return _lookup("Scripts", "Script", chr, "Unknown")


def proplist(chr):
    return _lookup("PropList", "Property", chr, "Unknown")


def category_alias(chr):
    cat = category(chr)
    return _alias("gc", cat)


def east_asian_width_alias(chr, default=None):
    eaw = east_asian_width(chr, default)
    return _alias("ea", eaw)


def bidirectional_alias(chr):
    bidi = bidirectional(chr)
    return _alias("bc", bidi)

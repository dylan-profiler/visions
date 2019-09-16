from functools import partial

import pandas as pd


def parse_range(x, pos):
    vals = x.split("..")
    if len(vals) == 1:
        vals.append(vals[0])
    vals = [int(x, 16) for x in vals]
    return vals[pos]


def _parse(file_name, names):
    df = pd.read_csv(
        file_name, sep=";", comment="#", names=names, skipinitialspace=True
    )
    if "range" in names:
        df["start"] = df["range"].apply(partial(parse_range, pos=0))
        df["end"] = df["range"].apply(partial(parse_range, pos=1))
    elif "idx" in names:
        df["idx"] = df["idx"].apply(partial(int, base=16))

    return df


def parse_unicode_data():
    return _parse(
        "data/UnicodeData.txt",
        [
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
    )


def parse_blocks():
    return _parse("data/Blocks.txt", ["range", "Block"])


def parse_property_value_aliases():
    return _parse(
        "data/PropertyValueAliases.txt",
        ["Property", "Short_Name", "Long_Name", "Alternative1", "Alternative2"],
    )


def parse_proplist():
    return _parse("data/PropList.txt", ["range", "Property"])


def parse_derived_core_properties():
    return _parse("data/DerivedCoreProperties.txt", ["range", "Derived_Property"])


def parse_line_break():
    return _parse("data/LineBreak.txt", ["range", "Line_Break"])


def parse_scripts():
    return _parse("data/Scripts.txt", ["range", "Script"])


def parse_script_extension():
    return _parse("data/ScriptExtension.txt", ["range", "Script_Extension"])


def parse_name_aliases():
    return _parse("data/NameAliases.txt", ["idx", "Alias", "Type"])


def parse_east_asian_width():
    return _parse("data/EastAsianWidth.txt", ["range", "East_Asian_Width"])


def _lookup(df, col, chr, default=None):
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


def _lookup_unicodedata(col, chr, default=None):
    df = parse_unicode_data()
    return _lookup(df, col, chr, default)


def _lookup_blocks(chr, default=None):
    df = parse_blocks()
    return _lookup(df, "Block", chr, default)


def _lookup_scripts(chr, default=None):
    df = parse_scripts()
    return _lookup(df, "Script", chr, default)


def _lookup_proplist(chr, default=None):
    df = parse_proplist()
    return _lookup(df, "Property", chr, default)


def name(chr, default=None):
    return _lookup_unicodedata("name", chr, default)


def category(chr):
    return _lookup_unicodedata("category", chr, "Zzzz")


def _alias(property, short_name):
    df = parse_property_value_aliases()
    df["Property"] = df["Property"].str.strip()
    df["Short_Name"] = df["Short_Name"].str.strip()
    try:
        return df[(df["Property"] == property) & (df["Short_Name"] == short_name)][
            "Long_Name"
        ].iloc[0]
    except IndexError:
        return None


def category_alias(chr):
    cat = category(chr)
    return _alias("gc", cat)


def bidirectional(chr):
    return _lookup_unicodedata("bidirectional", chr, "")


def decimal(chr, default=None):
    return _lookup_unicodedata("decimal", chr, default)


def digit(chr, default=None):
    return _lookup_unicodedata("digit", chr, default)


def numeric(chr, default=None):
    return _lookup_unicodedata("numeric", chr, default)


def east_asian_width(chr, default=None):
    df = parse_east_asian_width()
    return _lookup(df, "East_Asian_Width", chr, default).strip()


def east_asian_width_alias(chr, default=None):
    eaw = east_asian_width(chr, default)
    return _alias("ea", eaw)


def bidirectional_alias(chr):
    bidi = bidirectional(chr)
    return _alias("bc", bidi)


def combining(chr):
    return _lookup_unicodedata("combining", chr, 0)


def mirrored(chr):
    return _lookup_unicodedata("mirrored", chr, 0)


def decomposition(chr):
    val = _lookup_unicodedata("decomposition", chr, 0)
    if str(val) == "nan":
        val = ""
    return val


def block(chr):
    return _lookup_blocks(chr, "Unknown")


def script(chr):
    return _lookup_scripts(chr, "Unknown")


def proplist(chr):
    return _lookup_proplist(chr, "Unknown")

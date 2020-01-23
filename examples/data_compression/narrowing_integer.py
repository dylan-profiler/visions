import pandas as pd


def to_int_smallest(series: pd.Series) -> pd.Series:
    max = series.max()
    min = series.min()

    if min >= 0:
        if series.hasnans:
            u = "U"
        else:
            u = "u"

        if max <= 255:
            n = 8
        elif max <= 65535:
            n = 16
        elif max <= 4294967295:
            n = 32
        else:
            n = 64
    else:
        u = ""
        if max <= 127:
            n = 8
        elif max <= 32767:
            n = 16
        elif max <= 2147483647:
            n = 32
        else:
            n = 64

    if series.hasnans:
        i = "I"
    else:
        i = "i"

    type_name = f"{u}{i}nt{n}"

    return series.astype(type_name)

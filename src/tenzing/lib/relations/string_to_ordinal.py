import pandas as pd

from tenzing.core.model.model_relation import relation_conf


def check_consecutive(l):
    return sorted(l) == list(range(min(l), max(l) + 1))


def is_ordinal_str(s):
    if s.str.len().max() == 1:
        unique_values = list(s[s.notna()].str.lower().unique())
        return "a" in unique_values and check_consecutive(list(map(ord, unique_values)))
    else:
        return False


def to_ordinal(series: pd.Series) -> pd.Series:
    return pd.Series(
        pd.Categorical(series, categories=sorted(series[series.notna()].unique()), ordered=True)
    )


def string_to_ordinal():
    return relation_conf(
        inferential=True,
        relationship=is_ordinal_str,
        transformer=to_ordinal
    )

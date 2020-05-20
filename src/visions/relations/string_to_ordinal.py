import pandas as pd

from visions.relations.relations import InferenceRelation
from visions.types.ordinal import to_ordinal


def check_consecutive(l: list) -> bool:
    return sorted(l) == list(range(min(l), max(l) + 1))


def is_ordinal_str(s: pd.Series) -> bool:
    if s.str.len().max() == 1:
        unique_values = list(s[s.notna()].str.lower().unique())
        return "a" in unique_values and check_consecutive(list(map(ord, unique_values)))
    else:
        return False


def string_to_ordinal(cls) -> InferenceRelation:
    from visions.types import String

    return InferenceRelation(
        type=cls,
        related_type=String,
        relationship=is_ordinal_str,
        transformer=to_ordinal,
    )

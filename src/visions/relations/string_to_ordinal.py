import pandas as pd

from visions.relations.relations import InferenceRelation
from visions.relations.relations_utils import values_are_consecutive
from visions.types.ordinal import to_ordinal


def is_ordinal_str(s: pd.Series, state: dict) -> bool:
    if s.str.len().max() == 1:
        unique_values = list(s[s.notna()].str.lower().unique())
        return "a" in unique_values and values_are_consecutive(
            list(map(ord, unique_values))
        )
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

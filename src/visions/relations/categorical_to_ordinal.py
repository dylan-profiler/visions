from visions.relations.relations import InferenceRelation
from visions.types.ordinal import to_ordinal


def check_consecutive(l) -> bool:
    return sorted(l) == list(range(min(l), max(l) + 1))


def is_ordinal_cat(c) -> bool:
    s = c.astype(str)
    if s.str.len().max() == 1:
        unique_values = list(s[s.notna()].str.lower().unique())
        return "a" in unique_values and check_consecutive(list(map(ord, unique_values)))
    else:
        return False


def categorical_to_ordinal(cls) -> InferenceRelation:
    from visions.types import Categorical

    return InferenceRelation(
        cls, Categorical, relationship=is_ordinal_cat, transformer=to_ordinal
    )

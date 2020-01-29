from visions.core.model.relations import InferenceRelation
from visions.core.implementations.types.visions_ordinal import to_ordinal


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
    from visions.core.implementations.types import visions_categorical

    return InferenceRelation(
        cls, visions_categorical, relationship=is_ordinal_cat, transformer=to_ordinal
    )

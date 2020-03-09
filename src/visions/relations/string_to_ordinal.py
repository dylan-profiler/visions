from visions.relations.relations import InferenceRelation
from visions.types.visions_ordinal import to_ordinal


def check_consecutive(l) -> bool:
    return sorted(l) == list(range(min(l), max(l) + 1))


def is_ordinal_str(s) -> bool:
    if s.str.len().max() == 1:
        unique_values = list(s[s.notna()].str.lower().unique())
        return "a" in unique_values and check_consecutive(list(map(ord, unique_values)))
    else:
        return False


def string_to_ordinal(cls) -> InferenceRelation:
    from visions.types import visions_string

    return InferenceRelation(
        cls, visions_string, relationship=is_ordinal_str, transformer=to_ordinal
    )

from visions.core.model.relations import InferenceRelation
from visions.core.implementations.types.visions_ordinal import to_ordinal


def check_consecutive(l) -> bool:
    return sorted(l) == list(range(min(l), max(l) + 1))


def is_ordinal_str(s) -> bool:
    if s.str.len().max() == 1:
        unique_values = list(s[s.notna()].str.lower().unique())
        return "a" in unique_values and check_consecutive(list(map(ord, unique_values)))
    else:
        return False


def string_to_ordinal() -> InferenceRelation:
    from visions.core.implementations.types import visions_ordinal, visions_string

    return InferenceRelation(
        visions_ordinal,
        visions_string,
        relationship=is_ordinal_str,
        transformer=to_ordinal,
    )

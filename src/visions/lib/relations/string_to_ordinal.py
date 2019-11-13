from visions.core.model.relations import TypeRelation
from visions.core.implementations.types import to_ordinal


def check_consecutive(l):
    return sorted(l) == list(range(min(l), max(l) + 1))


def is_ordinal_str(s):
    if s.str.len().max() == 1:
        unique_values = list(s[s.notna()].str.lower().unique())
        return "a" in unique_values and check_consecutive(list(map(ord, unique_values)))
    else:
        return False


def string_to_ordinal():
    return TypeRelation(
        inferential=True, relationship=is_ordinal_str, transformer=to_ordinal
    )

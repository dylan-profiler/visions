from visions.core.model.relations import TypeRelation
from visions.core.implementations.types import to_ordinal


def check_consecutive(l):
    return sorted(l) == list(range(min(l), max(l) + 1))


def is_ordinal_int(s):
    unique_values = list(s.unique())
    return (
        check_consecutive(unique_values)
        and 2 < len(unique_values) < 10
        and 1 in unique_values
    )


def integer_to_ordinal():
    return TypeRelation(
        inferential=True, relationship=is_ordinal_int, transformer=to_ordinal
    )

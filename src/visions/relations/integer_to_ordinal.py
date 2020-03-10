from visions.relations import InferenceRelation
from visions.types.ordinal import to_ordinal


def check_consecutive(l) -> bool:
    return sorted(l) == list(range(min(l), max(l) + 1))


def is_ordinal_int(s) -> bool:
    unique_values = list(s.unique())
    return (
        check_consecutive(unique_values)
        and 2 < len(unique_values) < 10
        and 1 in unique_values
    )


def integer_to_ordinal(cls) -> InferenceRelation:
    from visions.types import Integer

    return InferenceRelation(
        cls, Integer, relationship=is_ordinal_int, transformer=to_ordinal
    )
